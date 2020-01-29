# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Initialization and entry-point for delete-cli."""


# type annotations
from __future__ import annotations
from typing import List

# standard libs
import os
import sys
import shutil
import sqlite3
import platform
import subprocess

# internal libs
from .logging import log
from .__meta__ import (__version__, __license__, __website__,
                       __copyright__, __description__)


# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError


PROGRAM = 'delete'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} PATH [PATH ...]
{__description__}\
"""

EPILOG = f"""\
Documentation and issue tracking at:
{__website__}

Copyright {__copyright__}. All rights reserved.
{__license__}.\
"""

HELP = f"""\
{USAGE}

arguments:
PATH                 A file or folder path.

actions:
    --list           List objects and their original path.
    --empty          Empty the trash.
    --restore        Restore one or more items.

options:
-h, --help           Show this message and exit.
-v, --version        Show the version and exit.

{EPILOG}\
"""


def log_error(exception: Exception, return_code: int = exit_status.runtime_error) -> int:
    """Log the exception and give the `return_code`."""
    log.error(f'{exception.__class__.__name__}: ' + ' - '.join(list(map(str, exception.args))))
    return return_code


# NOTE: in 2020 it is still unclear how best to remove folders in a clean and
#       cross platform way that isn't unnecessarily time consuming. Crawling
#       the file tree and doing checks to forcibly remove the folder *in the
#       Python layer* is slow and resource intensive. While seemingly brutish
#       at first, it seems the best implementation is simply to check platform
#       and run a system command.
if platform.system() == 'Windows':
    _rm_cmd = ['rmdir', '/S', '/Q']
else:
    _rm_cmd = ['rm', '-rf']

def rmdir(path: str) -> None:
    """Forcibly remove directory."""
    subprocess.run([*_rm_cmd, path])



CREATE_TABLE = """\
CREATE TABLE IF NOT EXISTS TRASH(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TIME DATETIME DEFAULT CURRENT_TIMESTAMP,
    NAME TEXT NOT NULL,
    PATH TEXT NOT NULL
);
"""

INSERT = """\
INSERT INTO TRASH(NAME, PATH) VALUES
("{0}", "{1}")
"""


class Delete(Application):
    """Application class for delete-cli."""

    interface = Interface(PROGRAM, USAGE, HELP)
    interface.add_argument('-v', '--version', action='version', version=__version__)

    paths: List[str] = []
    interface.add_argument('paths', nargs='*')

    do_list: bool = False
    do_empty: bool = False
    do_restore: bool = False
    actions = ['list', 'empty', 'restore']
    action_interface = interface.add_mutually_exclusive_group()
    action_interface.add_argument('--list', action='store_true', dest='do_list')
    action_interface.add_argument('--empty', action='store_true', dest='do_empty')
    action_interface.add_argument('--restore', action='store_true', dest='do_restore')

    exceptions = {
        RuntimeError: log_error,
        PermissionError: log_error,
    }

    # path to trash folder
    trash_path: str = os.getenv('TRASH_FOLDER',
                                 os.path.join(os.getenv('HOME'), '.Trash'))
    # path to sqlite3 database
    database_path: str = os.getenv('TRASH_DATABASE',
                                   trash_path.rstrip(os.path.pathsep) + '.db')

    def run(self) -> None:
        """Delegate actions."""

        for action in self.actions:
            if getattr(self, f'do_{action}') is True:
                method = getattr(self, f'{action}_action')
                method()
                return

        for path in self.paths:
            self.move_to_trash(path)

    def list_action(self) -> None:
        """List files from database."""

        if self.paths:
            raise ArgumentError('unexpected arguments: ' + ', '.join(self.paths))

        cursor = self.database.execute('SELECT * FROM TRASH')
        for *metadata, name, fullpath in cursor.fetchall():
            print(f'{name} -> {fullpath}')

    def empty_action(self) -> None:
        """Empty the trash folder and clear database."""

        if self.paths:
            raise ArgumentError('unexpected arguments: ' + ', '.join(self.paths))

        # unlink all files and folders in trash
        cursor = self.database.execute('SELECT * FROM TRASH')
        contents = cursor.fetchall()
        for *metadata, name, fullpath in contents:
            path = os.path.join(self.trash_path, name)
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                rmdir(path)
            else:
                os.remove(path)

        log.ok(f'removed {len(contents)} items from {self.trash_path}')

        # purge database
        cursor.execute('DROP TABLE TRASH')
        cursor.execute(CREATE_TABLE)  # so queries do not fail

        # warn on remaining items
        try:
            remaining = len(os.listdir(self.trash_path))
            if remaining > 0:
                log.error(f'{remaining} items still in {self.trash_path}')
        except PermissionError:
            # NOTE: macOS pitches a fit trying reading ~/.Trash
            log.error(f'permission denied: could not list {self.trash_path}')
            return

    def restore_action(self) -> None:
        """Restore all named items."""
        for path in self.paths:
            self.restore(path)

    def restore(self, path: str) -> None:
        """Delagate restore based on invocation."""
        if path.startswith(self.trash_path):
            self.restore_from_trash(path)
        elif os.path.exists(os.path.join(self.trash_path, path)):
            self.restore_from_trash(path)
        else:
            self.restore_from_original(path)

    def restore_from_trash(self, path: str) -> None:
        """Restore item from path in trash."""

        if not path.startswith(self.trash_path):
            fullpath = os.path.join(self.trash_path, path)
        else:
            fullpath = path
        if not os.path.exists(fullpath):
            log.error(f'{fullpath} does not exist')
            return

        basename = os.path.basename(fullpath)
        cursor = self.database.cursor()
        try:

            cursor.execute('BEGIN')
            cursor.execute(f'SELECT * FROM TRASH WHERE NAME = "{basename}"')

            results = cursor.fetchall()
            if not results:
                log.error(f'not found: {fullpath}')
                return
            if len(results) > 1:
                log.error(f'duplicate: {basename}')
                return

            *metadata, name, original_path = results[0]
            if os.path.exists(original_path):
                log.error(f'{original_path} already exists')
                return

            shutil.move(fullpath, original_path)
            cursor.execute(f'DELETE FROM trash WHERE NAME = "{basename}"')
            cursor.execute('COMMIT')
            log.ok(f'{fullpath} -> {original_path}')

        except self.database.Error:
            log.error(f'database: {fullpath} -> ?')
            cursor.execute('ROLLBACK')

        finally:
            cursor.close()

    def restore_from_original(self, path: str) -> None:
        """Restore file based on it's original path."""

        fullpath = os.path.abspath(path)
        cursor = self.database.cursor()
        try:

            cursor.execute('BEGIN')
            cursor.execute(f'SELECT * FROM TRASH WHERE PATH = "{fullpath}"')

            results = cursor.fetchall()
            if not results:
                log.error(f'database: {fullpath} not an original path')
                return
            if len(results) > 1:
                log.error(f'database: duplicates found for {fullpath}')
                return

            *metadata, name, original_path = results[0]
            if os.path.exists(original_path):
                log.error(f'{original_path} already exists')
                return

            shutil.move(fullpath, original_path)
            cursor.execute(f'DELETE FROM trash WHERE PATH = "{fullpath}"')
            cursor.execute('COMMIT')
            log.ok(f'{fullpath} -> {original_path}')

        except self.database.Error:
            log.error(f'{fullpath} -> ?')
            cursor.execute('ROLLBACK')

        finally:
            cursor.close()

    def move_to_trash(self, path: str) -> None:
        """Move a file/folder to the trash."""

        if not os.path.exists(path):
            log.error(f'{path} does not exist')
            return

        # find a unique destination path
        # any existing file in the trash with the same basename
        # will result in a numerical suffix being added BEFORE any EXTENSION
        basename = os.path.basename(path)
        destination = os.path.join(self.trash_path, basename)
        path_suffix = 1
        while os.path.exists(destination):
            filepath, ext = os.path.splitext(os.path.join(self.trash_path, basename))
            destination = f'{filepath}.{path_suffix}{ext}'
            path_suffix += 1

        # move the file/folder
        shutil.move(path, destination)

        # record to database
        cursor = self.database.cursor()
        cursor.execute('BEGIN')
        try:
            basename = os.path.basename(destination)
            fullpath = os.path.abspath(path)
            cursor.execute(INSERT.format(basename, fullpath))
            cursor.execute('COMMIT')
            log.ok(f'{path} -> {destination}')
        except self.database.Error:
            log.error(f'{path} -> {self.database_path}')
            cursor.execute('ROLLBACK')
        finally:
            cursor.close()

    def __enter__(self) -> Delete:
        """Resource initialization."""

        # ensure the trash folder exists
        if not os.path.exists(self.trash_path):
            os.makedirs(self.trash_path, exist_ok=True)
            log.ok(f'created {self.trash_path}')

        # initialize the database
        self.database = sqlite3.connect(self.database_path)
        self.database.isolation_level = None
        self.database.execute(CREATE_TABLE)
        return self

    def __exit__(self, *exc) -> None:
        """Release resources."""
        self.database.close()


def main() -> int:
    """Entry-point for delete-cli."""
    return Delete.main(sys.argv[1:])

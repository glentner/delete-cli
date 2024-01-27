# SPDX-FileCopyrightText: 2024 Geoffrey Lentner
# SPDX-License-Identifier: MIT

"""Simple command-line move-to-trash."""


# Type annotations
from __future__ import annotations
from typing import List

# Standard libs
import os
import sys
import shutil
import sqlite3
import platform
import subprocess
import importlib.metadata

# External libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError

# Internal libs
from delete.logging import logger as log

# Metadata
__appname__ = 'del'
__version__ = importlib.metadata.version('delete-cli')


USAGE = f"""\
Usage:
  {__appname__} [-hv] PATH [PATH ...]
  {__appname__} --restore PATH [PATH ...]
  {__appname__} --list
  {__appname__} --empty
  
  {__doc__}\
"""

HELP = f"""\
{USAGE}

Arguments:
  PATH               A file or folder path.

Actions:
  -l, --list         List objects and their original path.
  -e, --empty        Empty the trash.
  -r, --restore      Restore one or more items.

Options:
  -v, --version      Show the version and exit.
  -h, --help         Show this message and exit.\
"""


def handle_exception(exception: Exception, return_code: int = exit_status.runtime_error) -> int:
    """Log the exception and give the `return_code`."""
    log.err(f'{exception.__class__.__name__}: ' + ' - '.join(list(map(str, exception.args))))
    return return_code


def log_critical(message: str) -> None:
    """Logging wrapper to include application name."""
    log.err(f'{__appname__}: {message}')


# NOTE: in 2024 it is still unclear how best to remove folders in a clean and
#       cross-platform way that isn't unnecessarily time-consuming. Crawling
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
(?, ?)
"""


class Delete(Application):
    """Application class for program."""

    interface = Interface(__appname__, USAGE, HELP)
    interface.add_argument('-v', '--version', action='version', version=__version__)

    paths: List[str] = []
    interface.add_argument('paths', nargs='*')

    do_list: bool = False
    do_empty: bool = False
    do_restore: bool = False
    actions = ['list', 'empty', 'restore']
    action_interface = interface.add_mutually_exclusive_group()
    action_interface.add_argument('-l', '--list', action='store_true', dest='do_list')
    action_interface.add_argument('--empty', action='store_true', dest='do_empty')
    action_interface.add_argument('-r', '--restore', action='store_true', dest='do_restore')

    exceptions = {
        RuntimeError: handle_exception,
        PermissionError: handle_exception,
    }

    home: str = os.getenv('HOME') or '.'
    trash_path: str = os.getenv('TRASH_FOLDER', os.path.join(home, '.Trash'))
    database_path: str = os.getenv('TRASH_DATABASE',
                                   trash_path.rstrip(os.path.pathsep) + '.db')

    log_critical = log_critical
    log_exception = log_critical

    db: sqlite3.Connection

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

        cursor = self.db.execute('SELECT * FROM TRASH')
        for *metadata, name, fullpath in cursor.fetchall():
            print(f'{name} -> {fullpath}')

    def empty_action(self) -> None:
        """Empty the trash folder and clear database."""

        if self.paths:
            raise ArgumentError('cannot provide paths on --empty action')

        # unlink all files and folders in trash
        cursor = self.db.execute('SELECT * FROM TRASH')
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

        # Truncate database
        cursor.execute('DROP TABLE TRASH')
        cursor.execute(CREATE_TABLE)

        try:
            remaining = len(os.listdir(self.trash_path))
            if remaining > 0:
                log.err(f'{remaining} items still in {self.trash_path}')
        except PermissionError:
            # NOTE: macOS pitches a fit trying to read ~/.Trash
            log.err(f'permission denied: could not list {self.trash_path}')
            return

    def restore_action(self) -> None:
        """Restore all named items."""
        for path in self.paths:
            self.restore(path)

    def restore(self, path: str) -> None:
        """Delegate restore based on invocation."""
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
            log.err(f'does not exit: {fullpath}')
            return

        basename = os.path.basename(fullpath)
        cursor = self.db.cursor()
        try:

            cursor.execute('BEGIN')
            cursor.execute(f'SELECT * FROM TRASH WHERE NAME = ?', (basename, ))

            results = cursor.fetchall()
            if not results:
                log.err(f'not found: {fullpath}')
                return
            if len(results) > 1:
                log.err(f'duplicate: {basename}')
                return

            *metadata, name, original_path = results[0]
            if os.path.exists(original_path):
                log.err(f'already exists: {original_path}')
                return

            shutil.move(fullpath, original_path)
            cursor.execute(f'DELETE FROM trash WHERE NAME = ?', (basename, ))
            cursor.execute('COMMIT')
            log.ok(f'{fullpath} -> {original_path}')

        except self.db.Error:
            log.err(f'db: {fullpath} -> ?')
            cursor.execute('ROLLBACK')

        finally:
            cursor.close()

    def restore_from_original(self, path: str) -> None:
        """Restore file based on its original path."""

        fullpath = os.path.abspath(path)
        cursor = self.db.cursor()
        try:

            cursor.execute('BEGIN')
            cursor.execute(f'SELECT * FROM TRASH WHERE PATH = ?', (fullpath, ))

            results = cursor.fetchall()
            if not results:
                log.err(f'db: {fullpath} not an original path')
                return
            if len(results) > 1:
                log.err(f'db: duplicates found for {fullpath}')
                return

            *metadata, name, original_path = results[0]
            if os.path.exists(original_path):
                log.err(f'already exists: {original_path}')
                return

            shutil.move(fullpath, original_path)
            cursor.execute(f'DELETE FROM trash WHERE PATH = ?', (fullpath, ))
            cursor.execute('COMMIT')
            log.ok(f'{fullpath} -> {original_path}')

        except self.db.Error:
            log.err(f'{fullpath} -> ?')
            cursor.execute('ROLLBACK')

        finally:
            cursor.close()

    def move_to_trash(self, path: str) -> None:
        """Move a file/folder to the trash."""

        if not os.path.exists(path):
            log.err(f'does not exist: {path}')
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
        cursor = self.db.cursor()
        cursor.execute('BEGIN')
        try:
            basename = os.path.basename(destination)
            fullpath = os.path.abspath(path)
            cursor.execute(INSERT, (basename, fullpath))
            cursor.execute('COMMIT')
            log.ok(f'{path} -> {destination}')
        except self.db.Error:
            log.err(f'{path} -> {self.database_path}')
            cursor.execute('ROLLBACK')
        finally:
            cursor.close()

    def __enter__(self) -> Delete:
        """Resource initialization."""

        if not os.path.exists(self.trash_path):
            os.makedirs(self.trash_path, exist_ok=True)
            log.ok(f'Created {self.trash_path}')

        self.db = sqlite3.connect(self.database_path)
        self.db.isolation_level = None
        self.db.execute(CREATE_TABLE)
        return self

    def __exit__(self, *exc) -> None:
        """Release resources."""
        self.db.close()


def main(argv: List[str] | None = None) -> int:
    """Entry-point for program."""
    return Delete.main(argv or sys.argv[1:])

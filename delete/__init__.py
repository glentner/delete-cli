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

# internal libs
from .logging import log
from .__meta__ import (__version__, __license__, __website__,
                       __copyright__, __description__)


# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface


PROGRAM = 'delete'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} PATH [PATH ...]
       {PADDING} [--help] [--version]

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

options:
-h, --help           Show this message and exit.
-v, --version        Show the version and exit.

{EPILOG}\
"""


def log_error(exception: Exception, return_code: int = exit_status.runtime_error) -> int:
    """Log the exception and give the `return_code`."""
    log.error(*exception.args)
    return return_code


class Delete(Application):
    """Application class for delete-cli."""

    interface = Interface(PROGRAM, USAGE, HELP)
    interface.add_argument('-v', '--version', action='version', version=__version__)

    paths: List[str] = []
    interface.add_argument('paths', nargs='+')

    trash_folder: str = os.getenv('TRASH_FOLDER', os.path.join(os.getenv('HOME'), '.Trash'))

    exceptions = {
        RuntimeError: log_error,
    }

    def run(self) -> None:
        """Top-level business logic of DeleteApp."""
        os.makedirs(self.trash_folder, exist_ok=True)
        for path in self.paths:
            self.move_to_trash(path)

    def move_to_trash(self, path: str) -> None:
        """Move a file/folder to the trash."""

        if not os.path.exists(path):
            log.error(f'{path} does not exist')
            return

        # find a unique destination path
        # any existing file in the trash with the same basename
        # will result in a numerical suffix being added BEFORE any EXTENSION
        basename = os.path.basename(path)
        destination = os.path.join(self.trash_folder, basename)
        path_suffix = 1
        while os.path.exists(destination):
            filepath, ext = os.path.splitext(os.path.join(self.trash_folder, basename))
            destination = f'{filepath}.{path_suffix}{ext}'
            path_suffix += 1

        # move the file/folder
        shutil.move(path, destination)
        log.ok(f'{path} -> {destination}')


def main() -> int:
    """Entry-point for delete-cli."""
    return Delete.main(sys.argv[1:])

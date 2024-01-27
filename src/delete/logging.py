# SPDX-FileCopyrightText: 2024 Geoffrey Lentner
# SPDX-License-Identifier: MIT

"""Custom logging behavior."""


# Type annotations
from __future__ import annotations

# Standard libs
from enum import Enum
import logging


OK = logging.INFO
ERR = logging.ERROR
logging.addLevelName(OK, 'OK')
logging.addLevelName(ERR, 'ERR')


@logging.setLoggerClass
class Logger(logging.Logger):
    """Extend Logger class to include new level methods."""

    def ok(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'OK'."""
        if self.isEnabledFor(OK):
            self._log(OK, msg, args, **kwargs)

    def err(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'ERR'."""
        if self.isEnabledFor(ERR):
            self._log(ERR, msg, args, **kwargs)


class Ansi(Enum):
    """ANSI escape sequences."""
    
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'


COLOR_BY_LEVEL = {
    'OK': Ansi.GREEN,
    'ERR': Ansi.RED
}


@logging.setLogRecordFactory
class LogRecord(logging.LogRecord):
    """Extends LogRecord to include ANSI color codes by level."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ansi_color = COLOR_BY_LEVEL[self.levelname].value
        self.ansi_reset = Ansi.RESET.value


handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(ansi_color)s%(levelname)s%(ansi_reset)s %(message)s')
)


logger = logging.getLogger('delete')
logger.setLevel(OK)
logger.addHandler(handler)

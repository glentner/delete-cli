# SPDX-FileCopyrightText: 2024 Geoffrey Lentner
# SPDX-License-Identifier: MIT

"""Custom logging behavior."""


# Type annotations
from __future__ import annotations
from typing import Dict, Final

# Standard libs
import logging

# External libs
from cmdkit.ansi import Ansi


OK: Final[int] = logging.INFO
ERR: Final[int] = logging.ERROR
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


COLOR_BY_LEVEL: Final[Dict[str, Ansi]] = {
    'OK': Ansi.GREEN,
    'ERR': Ansi.RED,
}


@logging.setLogRecordFactory
class LogRecord(logging.LogRecord):
    """Extends LogRecord to include ANSI color codes by level."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ansi_reset = Ansi.RESET.value
        if self.levelname in COLOR_BY_LEVEL:
            self.ansi_color = COLOR_BY_LEVEL[self.levelname].value
        else:
            self.ansi_color = ''


handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(ansi_color)s%(levelname)s%(ansi_reset)s %(message)s')
)


logger = logging.getLogger('delete')
logger.setLevel(OK)
logger.addHandler(handler)

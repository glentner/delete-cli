# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Logging functionality."""

# standard libs
import sys
from dataclasses import dataclass
from typing import Tuple, IO

# external libs
from logalpha import levels as _levels
from logalpha import colors as _colors
from logalpha import messages as _messages
from logalpha import handlers as _handlers
from logalpha import loggers as _loggers



class Logger(_loggers.Logger):
    """Logging interface."""

    levels: Tuple[_levels.Level] = _levels.Level.from_names(['OK', 'ERROR'])
    colors: Tuple[_colors.Color] = _colors.Color.from_names(['green', 'red'])


@dataclass
class Handler(_handlers.Handler):
    """OK/ERROR messages printed to stderr."""

    level: _levels.Level = Logger.levels[0]
    resource: IO = sys.stderr

    def format(self, msg: _messages.Message) -> str:
        """Format message with OK/ERROR."""
        COLOR_CODE = Logger.colors[msg.level.value].foreground
        COLOR_RESET = _colors.ANSI_RESET
        return f'{COLOR_CODE}{msg.level.name}{COLOR_RESET} {msg.content}'


log = Logger()
log.handlers.append(Handler())

# inject logger back into cmdkit
from cmdkit import logging as _cmd_logging, app as _cmd_app
_cmd_logging.log = log
_cmd_app.Application.log_error = log.error

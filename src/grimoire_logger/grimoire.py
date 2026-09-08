from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import lru_cache
import json
import os.path
import sys
from typing import Optional, TextIO


class LogLevel(Enum):
    info = 1
    warn = 2
    error = 3
    debug = 4


# Keep the public enum values unchanged, but use conventional severity for
# filtering so ``Logger(min_level=LogLevel.info)`` suppresses debug messages.
_SEVERITY = {
    LogLevel.debug: 10,
    LogLevel.info: 20,
    LogLevel.warn: 30,
    LogLevel.error: 40,
}


@dataclass
class Logger:
    """A small, fast JSON logger.

    ``min_level`` is optional so the default behaviour stays backwards
    compatible. When it is set, filtered messages return before inspecting the
    call stack, formatting JSON, or writing to the output stream.
    """

    min_level: Optional[LogLevel] = None
    stream: Optional[TextIO] = None

    def info(self, message: str = '') -> None:
        self._log(LogLevel.info, message)

    def warn(self, message: str = '') -> None:
        self._log(LogLevel.warn, message)

    def error(self, message: str = '') -> None:
        self._log(LogLevel.error, message)

    def debug(self, message: str = '') -> None:
        self._log(LogLevel.debug, message)

    def _log(self, log_level: LogLevel, message: str) -> None:
        if not self._is_enabled(log_level):
            return

        # The caller is two frames above this method (``_log`` -> level
        # method -> application code). This is substantially cheaper than
        # inspect.stack(), which creates FrameInfo objects for the whole stack.
        caller_frame = sys._getframe(2)
        log_message = generate_log(log_level, message, caller_frame)

        if self.stream is None:
            print(log_message)
        else:
            print(log_message, file=self.stream)

    def _is_enabled(self, log_level: LogLevel) -> bool:
        if self.min_level is None:
            return True

        return _SEVERITY[log_level] >= _SEVERITY[self.min_level]


@lru_cache(maxsize=256)
def _source_name(filename: str) -> str:
    """Return the existing source format without repeating path work."""
    return os.path.splitext(os.path.basename(filename))[0] + '.py'


def generate_log(
    log_level: LogLevel,
    message: str,
    caller_frame=None,
) -> str:
    """Generate one JSON log entry.

    ``caller_frame`` is used internally to avoid walking the stack twice. It
    remains optional so the original helper can still be called directly.
    """
    if caller_frame is None:
        caller_frame = sys._getframe(1)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    source = _source_name(caller_frame.f_code.co_filename)

    log = {
        'timestamp': timestamp,
        'level': log_level.name,
        'source': source,
    }
    if log_level == LogLevel.debug:
        log['line'] = caller_frame.f_lineno
    log['message'] = message

    # Compact JSON reduces log volume while json.dumps correctly escapes
    # quotes, newlines, backslashes, and non-ASCII messages.
    return json.dumps(log, ensure_ascii=False, separators=(',', ':'))

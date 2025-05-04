from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from inspect import getframeinfo
import inspect
import os.path
import sys


class LogLevel(Enum):
    info = 1
    warn = 2
    error = 3
    debug = 4

@dataclass
class Logger:
    def info(self, message: str = '') -> 'LogWithLine':
        log_message = generate_log(LogLevel.info, message)
        print(log_message)
        return LogWithLine(log_message)

    def warn(self, message: str = '') -> 'LogWithLine':
        log_message = generate_log(LogLevel.warn, message)
        print(log_message)
        return LogWithLine(log_message)

    def error(self, message: str = '') -> 'LogWithLine':
        log_message = generate_log(LogLevel.error, message)
        print(log_message, file=sys.stderr)
        return LogWithLine(log_message)

    def debug(self, message: str = '') -> 'LogWithLine':
        log_message = generate_log(LogLevel.debug, message)
        print(log_message)
        return LogWithLine(log_message)

class LogWithLine:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def line(self) -> None:
        caller = getframeinfo(inspect.stack()[1][0])
        log_with_line = f'{self.log_message[:-1]}, "line": {caller.lineno}}}'
        print(log_with_line)


def generate_log(log_level: LogLevel, message: str) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = f'{{"timestamp": "{timestamp}", "level": "{log_level.name}", "source": "{os.path.splitext(os.path.basename(inspect.stack()[2].filename))[0]}.py", "message": "{message}"}}'
    return log

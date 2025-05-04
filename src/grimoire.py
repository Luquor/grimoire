from enum import Enum
from datetime import datetime
from inspect import getframeinfo
from dataclasses import dataclass
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
    def info(self, message: str = '') -> None:
        log_message = generate_log(LogLevel.info, message)
        print(log_message)

    def warn(self, message: str = '') -> None:
        log_message = generate_log(LogLevel.warn, message)
        print(log_message)

    def error(self, message: str = '') -> None:
        log_message = generate_log(LogLevel.error, message)
        print(log_message)

    def debug(self, message: str = '') -> None:
        log_message = generate_log(LogLevel.debug, message)
        print(log_message)

def generate_log(log_level: LogLevel, message: str) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    caller_frame = inspect.stack()[2]
    filename = os.path.basename(caller_frame.filename)
    source = os.path.splitext(filename)[0]
    
    line_info = ""
    if log_level == LogLevel.debug:
        line_number = caller_frame.lineno
        line_info = f", \"line\": {line_number}"
    
    log = f'{{"timestamp": "{timestamp}", "level": "{log_level.name}", "source": "{source}.py"{line_info}, "message": "{message}"}}'
    return log
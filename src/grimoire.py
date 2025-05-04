from enum import Enum
from datetime import datetime
import inspect
import os.path
from dataclasses import dataclass
import sys


class LogLevel(Enum):
    info = 1
    warn = 2
    error = 3
    debug = 4

@dataclass
class Logger:
    def info(self, message: str = '') -> None:
        print(generate_log(LogLevel.info, message))

    def warn(self, message: str = '') -> None:
        print(generate_log(LogLevel.warn, message))

    def error(self, message: str = '') -> None:
        print(generate_log(LogLevel.error, message), file=sys.stderr)

    def debug(self, message: str = '') -> None:
        print(generate_log(LogLevel.debug, message))


def generate_log(log_level: LogLevel, message: str) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = f'{{"timestamp": "{timestamp}", "level": "{log_level.name}", "source": "{os.path.splitext(os.path.basename(inspect.stack()[2].filename))[0]}.py", "message": "{message}"}}'
    return log

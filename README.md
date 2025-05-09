# Grimoire Logger

Grimoire Logger is a lightweight Python logging library that outputs logs in a
structured JSON format. It is designed to make log parsing and analysis easier,
especially in distributed systems or environments where structured logging is
essential.

## Features

- **JSON-formatted logs**: Logs are output in a machine-readable JSON format.
- **Multiple log levels**: Supports `info`, `warn`, `error`, and `debug` levels.
- **Timestamped logs**: Each log entry includes a timestamp for better
  traceability.
- **Source identification**: Automatically includes the source file in the log
  output.

## Installation

You can install Grimoire Logger by cloning this repository to a local place or
by using `pip`:

```bash
pip install grimoire_logger
```

## Usage

Here’s a quick example of how to use Grimoire Logger:

```python
from grimoire_logger import Logger

log = Logger()

log.info("This is an info message")
log.debug("This is a debug message")
log.warn("This is a warning message")
log.error("This is an error message")
```

This code will output the following:

```json
$ python main.py
{"timestamp": "2025-05-04 18:31:14", "level": "info", "source": "main.py", "message": "This is an info message"}
{"timestamp": "2025-05-04 18:31:14", "level": "debug", "source": "main.py", "line": 6, "message": "This is a debug message"}
{"timestamp": "2025-05-04 18:31:14", "level": "warn", "source": "main.py", "message": "This is a warning message"}
{"timestamp": "2025-05-04 18:31:14", "level": "error", "source": "main.py", "message": "This is an error message"}
```

It is a design purpose that only the debug level prints the line of thet caller.

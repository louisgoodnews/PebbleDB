"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import os

from pathlib import Path
from typing import Final, Literal

from core.utils import PebbleCommitService


__all__: Final[list] = [
    "BOOLEAN",
    "CUSTOM",
    "CWD",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "DICTIONARY",
    "FLOAT",
    "INTEGER",
    "LIST",
    "MISSING",
    "NULL",
    "PATH",
    "PEBBLE_COMMIT_SERVICE",
    "STRING",
    "TIME",
    "UUID",
]


# Initialize the boolean field type as a module constant
BOOLEAN: Final[Literal["boolean"]] = "boolean"

# Initialize the custom field type as a module constant
CUSTOM: Final[Literal["custom"]] = "custom"

# Initialize the current working directory as module Path constant
CWD: Final[Path] = Path(os.getcwd())

# Initialize the date field type as a module constant
DATE: Final[Literal["date"]] = "date"

# Initialize the datetime field type as a module constant
DATETIME: Final[Literal["datetime"]] = "datetime"

# Initialize the decimal field type as a module constant
DECIMAL: Final[Literal["decimal"]] = "decimal"

# Initialize the dictionary field type as a module constant
DICTIONARY: Final[Literal["dictionary"]] = "dictionary"

# Initialize the float field type as a module constant
FLOAT: Final[Literal["float"]] = "float"

# Initialize the integer field type as a module constant
INTEGER: Final[Literal["integer"]] = "integer"

# Initialize the list field type as a module constant
LIST: Final[Literal["list"]] = "list"

# Initialize the missing value as a module constant
MISSING: Final[object] = object()

# Initialize the null field type as a module constant
NULL: Final[Literal["null"]] = "null"

# Initialize the path field type as a module constant
PATH: Final[Literal["path"]] = "path"

# Initialize the PebbleCommitService instance as a module constant
PEBBLE_COMMIT_SERVICE: Final[PebbleCommitService] = PebbleCommitService()

# Initialize the string field type as a module constant
STRING: Final[Literal["string"]] = "string"

# Initialize the time field type as a module constant
TIME: Final[Literal["time"]] = "time"

# Initialize the UUID field type as a module constant
UUID: Final[Literal["uuid"]] = "uuid"

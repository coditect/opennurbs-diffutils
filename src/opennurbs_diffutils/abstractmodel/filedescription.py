from datetime import datetime
from pathlib import Path
import re
from typing import Tuple


# 2002-02-21 23:30:39.942229878 -0800
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
PARSE_PATTERN = re.compile(
    r"^(\+{3}|-{3})\s+(.+?)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ [+-]\d+)"
)


class FileDescription:

    __slots__ = ("path", "time")

    def __init__(self, path: Path, time: datetime = None):
        self.path = path
        self.time = (
            time
            if time is not None
            else datetime.fromtimestamp(path.stat().st_mtime).astimezone()
        )

    def __str__(self) -> str:
        if self.time:
            return f"{self.path} {self.timestamp}"
        return self.path

    def label(self, label: str):
        self.path = label
        self.time = None

    @property
    def timestamp(self) -> str:
        return self.time.strftime(TIMESTAMP_FORMAT)

    @classmethod
    def fromString(cls, string: str) -> Tuple["FileDescription", str]:
        match = PARSE_PATTERN.match(string)
        if match:
            path = Path(match[2])
            time = datetime.strptime(match[3], TIMESTAMP_FORMAT)
            return cls(path, time), match[1]
        return None

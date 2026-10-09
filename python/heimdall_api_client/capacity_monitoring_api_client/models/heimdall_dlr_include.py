from enum import Enum


class HeimdallDlrInclude(str, Enum):
    SPANS = "spans"

    def __str__(self) -> str:
        return str(self.value)

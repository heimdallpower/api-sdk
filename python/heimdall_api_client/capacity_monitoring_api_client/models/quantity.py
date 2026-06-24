from enum import Enum


class Quantity(str, Enum):
    APPARENT_POWER = "apparent_power"
    CURRENT = "current"

    def __str__(self) -> str:
        return str(self.value)

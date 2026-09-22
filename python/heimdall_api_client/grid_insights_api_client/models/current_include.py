from enum import Enum


class CurrentInclude(str, Enum):
    MEASUREMENT_POINTS = "measurement_points"

    def __str__(self) -> str:
        return str(self.value)

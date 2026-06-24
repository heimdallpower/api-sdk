from enum import Enum


class CapacityMonitoringV1LinesGetHeimdallDlrsXRegion(str, Enum):
    EU = "eu"
    US = "us"

    def __str__(self) -> str:
        return str(self.value)

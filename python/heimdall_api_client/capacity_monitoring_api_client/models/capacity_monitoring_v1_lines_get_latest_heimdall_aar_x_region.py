from enum import Enum


class CapacityMonitoringV1LinesGetLatestHeimdallAarXRegion(str, Enum):
    EU = "eu"
    US = "us"

    def __str__(self) -> str:
        return str(self.value)

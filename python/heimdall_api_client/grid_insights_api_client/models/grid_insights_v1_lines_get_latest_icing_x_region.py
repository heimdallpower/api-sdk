from enum import Enum


class GridInsightsV1LinesGetLatestIcingXRegion(str, Enum):
    EU = "eu"
    US = "us"

    def __str__(self) -> str:
        return str(self.value)

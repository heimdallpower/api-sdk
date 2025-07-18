from enum import Enum

class GridInsightsV1LinesGetLatestConductorTemperatureXRegion(str, Enum):
    EU = "eu"
    US = "us"

    def __str__(self) -> str:
        return str(self.value)

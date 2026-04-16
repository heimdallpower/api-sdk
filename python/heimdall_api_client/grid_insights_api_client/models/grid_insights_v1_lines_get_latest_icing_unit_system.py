from enum import Enum


class GridInsightsV1LinesGetLatestIcingUnitSystem(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"

    def __str__(self) -> str:
        return str(self.value)

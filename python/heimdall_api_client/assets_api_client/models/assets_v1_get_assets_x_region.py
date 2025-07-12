from enum import Enum

class AssetsV1GetAssetsXRegion(str, Enum):
    EU = "eu"
    US = "us"

    def __str__(self) -> str:
        return str(self.value)

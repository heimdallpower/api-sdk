from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.latest_line_current import LatestLineCurrent


T = TypeVar("T", bound="GridInsightsV1LinesGetLatestCurrentResponse200")


@_attrs_define
class GridInsightsV1LinesGetLatestCurrentResponse200:
    """
    Attributes:
        data (LatestLineCurrent):
    """

    data: "LatestLineCurrent"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_line_current import LatestLineCurrent

        d = dict(src_dict)
        data = LatestLineCurrent.from_dict(d.pop("data"))

        grid_insights_v1_lines_get_latest_current_response_200 = cls(
            data=data,
        )

        grid_insights_v1_lines_get_latest_current_response_200.additional_properties = d
        return grid_insights_v1_lines_get_latest_current_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

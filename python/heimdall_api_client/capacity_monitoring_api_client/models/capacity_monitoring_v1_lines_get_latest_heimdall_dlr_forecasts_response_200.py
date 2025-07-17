from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.heimdall_dlr_forecasts import HeimdallDlrForecasts





T = TypeVar("T", bound="CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200")



@_attrs_define
class CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200:
    """ 
        Attributes:
            data (HeimdallDlrForecasts):
     """

    data: 'HeimdallDlrForecasts'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.heimdall_dlr_forecasts import HeimdallDlrForecasts
        data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_dlr_forecasts import HeimdallDlrForecasts
        d = dict(src_dict)
        data = HeimdallDlrForecasts.from_dict(d.pop("data"))




        capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts_response_200 = cls(
            data=data,
        )


        capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts_response_200.additional_properties = d
        return capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts_response_200

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

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.latest_heimdall_dlr import LatestHeimdallDlr





T = TypeVar("T", bound="CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200")



@_attrs_define
class CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200:
    """ 
        Attributes:
            data (LatestHeimdallDlr):
     """

    data: 'LatestHeimdallDlr'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_heimdall_dlr import LatestHeimdallDlr
        d = dict(src_dict)
        data = LatestHeimdallDlr.from_dict(d.pop("data"))




        capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200 = cls(
            data=data,
        )


        capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200.additional_properties = d
        return capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200

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

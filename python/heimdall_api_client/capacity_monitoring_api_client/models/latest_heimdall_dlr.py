from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.heimdall_dlr import HeimdallDlr





T = TypeVar("T", bound="LatestHeimdallDlr")



@_attrs_define
class LatestHeimdallDlr:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Heimdall DLR.
            unit (str): The unit of the value in the response. Example: Ampere.
            heimdall_dlr (HeimdallDlr):
     """

    metric: str
    unit: str
    heimdall_dlr: 'HeimdallDlr'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        heimdall_dlr = self.heimdall_dlr.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "heimdall_dlr": heimdall_dlr,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_dlr import HeimdallDlr
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        heimdall_dlr = HeimdallDlr.from_dict(d.pop("heimdall_dlr"))




        latest_heimdall_dlr = cls(
            metric=metric,
            unit=unit,
            heimdall_dlr=heimdall_dlr,
        )


        latest_heimdall_dlr.additional_properties = d
        return latest_heimdall_dlr

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

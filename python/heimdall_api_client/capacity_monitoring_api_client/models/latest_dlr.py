from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.dlr import Dlr





T = TypeVar("T", bound="LatestDlr")



@_attrs_define
class LatestDlr:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Heimdall DLR.
            unit (str): The unit of the value in the response. Example: Ampere.
            dlr (Dlr):
     """

    metric: str
    unit: str
    dlr: 'Dlr'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.dlr import Dlr
        metric = self.metric

        unit = self.unit

        dlr = self.dlr.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "dlr": dlr,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dlr import Dlr
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        dlr = Dlr.from_dict(d.pop("dlr"))




        latest_dlr = cls(
            metric=metric,
            unit=unit,
            dlr=dlr,
        )


        latest_dlr.additional_properties = d
        return latest_dlr

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

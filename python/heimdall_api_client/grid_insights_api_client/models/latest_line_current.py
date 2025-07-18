from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.line_current import LineCurrent





T = TypeVar("T", bound="LatestLineCurrent")



@_attrs_define
class LatestLineCurrent:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Current.
            unit (str): The unit of the value in the response. Example: Ampere.
            current (LineCurrent):
     """

    metric: str
    unit: str
    current: 'LineCurrent'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        current = self.current.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "current": current,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_current import LineCurrent
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        current = LineCurrent.from_dict(d.pop("current"))




        latest_line_current = cls(
            metric=metric,
            unit=unit,
            current=current,
        )


        latest_line_current.additional_properties = d
        return latest_line_current

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

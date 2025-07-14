from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.span import Span





T = TypeVar("T", bound="Line")



@_attrs_define
class Line:
    """ 
        Attributes:
            id (UUID): Unique identifier of the line. Example: 00000000-0000-0000-0000-000000000000.
            name (str): Name of the line. Example: Line A.
            available_forecast_hours (int): The available forecast length in hours, used as a query parameter for DLR
                forecasts. The maximum is 240 hours. Example: 72.
            spans (list['Span']): List of spans belonging to the line.
     """

    id: UUID
    name: str
    available_forecast_hours: int
    spans: list['Span']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.span import Span
        id = str(self.id)

        name = self.name

        available_forecast_hours = self.available_forecast_hours

        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "available_forecast_hours": available_forecast_hours,
            "spans": spans,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span import Span
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        available_forecast_hours = d.pop("available_forecast_hours")

        spans = []
        _spans = d.pop("spans")
        for spans_item_data in (_spans):
            spans_item = Span.from_dict(spans_item_data)



            spans.append(spans_item)


        line = cls(
            id=id,
            name=name,
            available_forecast_hours=available_forecast_hours,
            spans=spans,
        )


        line.additional_properties = d
        return line

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

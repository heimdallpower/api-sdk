from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from uuid import UUID






T = TypeVar("T", bound="ProbabilisticLineAmpacity")



@_attrs_define
class ProbabilisticLineAmpacity:
    """ 
        Attributes:
            value (float): The ampacity value (in amperes) for the line. Example: 375.4.
            at_span_id (UUID): Identifier of the span at which this ampacity forecast was calculated. The forecast is
                computed per span and timestamp, and the final dimensioning value is determined by selecting the span with the
                lowest ampacity. Example: 00000000-0000-0000-0000-000000000000.
     """

    value: float
    at_span_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        value = self.value

        at_span_id = str(self.at_span_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "at_span_id": at_span_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        at_span_id = UUID(d.pop("at_span_id"))




        probabilistic_line_ampacity = cls(
            value=value,
            at_span_id=at_span_id,
        )


        probabilistic_line_ampacity.additional_properties = d
        return probabilistic_line_ampacity

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

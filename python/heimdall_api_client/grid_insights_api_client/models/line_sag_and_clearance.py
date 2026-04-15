from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.span_sag_and_clearance import SpanSagAndClearance


T = TypeVar("T", bound="LineSagAndClearance")


@_attrs_define
class LineSagAndClearance:
    """
    Attributes:
        spans (list[SpanSagAndClearance]): List of spans on the line with their sag and clearance data.
    """

    spans: list["SpanSagAndClearance"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "spans": spans,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_sag_and_clearance import SpanSagAndClearance

        d = dict(src_dict)
        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:
            spans_item = SpanSagAndClearance.from_dict(spans_item_data)
            spans.append(spans_item)

        line_sag_and_clearance = cls(
            spans=spans,
        )

        line_sag_and_clearance.additional_properties = d
        return line_sag_and_clearance

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

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from uuid import UUID

if TYPE_CHECKING:
    from ..models.span_phase_sag_and_clearance import SpanPhaseSagAndClearance


T = TypeVar("T", bound="SpanSagAndClearance")


@_attrs_define
class SpanSagAndClearance:
    """
    Attributes:
        span_id (UUID): The id of the span.
        span_phases (list[SpanPhaseSagAndClearance]): List of span phases (conductors) within this span.
    """

    span_id: UUID
    span_phases: list["SpanPhaseSagAndClearance"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_id = str(self.span_id)

        span_phases = []
        for span_phases_item_data in self.span_phases:
            span_phases_item = span_phases_item_data.to_dict()
            span_phases.append(span_phases_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_id": span_id,
                "span_phases": span_phases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_phase_sag_and_clearance import SpanPhaseSagAndClearance

        d = dict(src_dict)
        span_id = UUID(d.pop("span_id"))

        span_phases = []
        _span_phases = d.pop("span_phases")
        for span_phases_item_data in _span_phases:
            span_phases_item = SpanPhaseSagAndClearance.from_dict(span_phases_item_data)
            span_phases.append(span_phases_item)

        span_sag_and_clearance = cls(
            span_id=span_id,
            span_phases=span_phases,
        )

        span_sag_and_clearance.additional_properties = d
        return span_sag_and_clearance

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

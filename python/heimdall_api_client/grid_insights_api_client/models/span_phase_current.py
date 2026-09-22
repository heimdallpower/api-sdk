from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.measurement_point_current import MeasurementPointCurrent


T = TypeVar("T", bound="SpanPhaseCurrent")


@_attrs_define
class SpanPhaseCurrent:
    """
    Attributes:
        span_phase_id (UUID): The id of the span phase. Example: 00000000-0000-0000-0000-000000000000.
        measurement_points (list[MeasurementPointCurrent]): Measurement points (one per sub-conductor) within this span
            phase.
    """

    span_phase_id: UUID
    measurement_points: list[MeasurementPointCurrent]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_phase_id = str(self.span_phase_id)

        measurement_points = []
        for measurement_points_item_data in self.measurement_points:
            measurement_points_item = measurement_points_item_data.to_dict()
            measurement_points.append(measurement_points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_phase_id": span_phase_id,
                "measurement_points": measurement_points,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.measurement_point_current import MeasurementPointCurrent

        d = dict(src_dict)
        span_phase_id = UUID(d.pop("span_phase_id"))

        measurement_points = []
        _measurement_points = d.pop("measurement_points")
        for measurement_points_item_data in _measurement_points:
            measurement_points_item = MeasurementPointCurrent.from_dict(measurement_points_item_data)

            measurement_points.append(measurement_points_item)

        span_phase_current = cls(
            span_phase_id=span_phase_id,
            measurement_points=measurement_points,
        )

        span_phase_current.additional_properties = d
        return span_phase_current

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

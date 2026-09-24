from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.measurement_point import MeasurementPoint


T = TypeVar("T", bound="SpanPhase")


@_attrs_define
class SpanPhase:
    """
    Attributes:
        id (UUID): Unique identifier of the span phase. Example: 00000000-0000-0000-0000-000000000000.
        measurement_points (list[MeasurementPoint]): List of measurement points belonging to the span phase. Empty if no
            Neuron has been installed on the span phase.
        name (None | str | Unset): Name of the span phase, defined by the grid owner. Example: Phase A.
    """

    id: UUID
    measurement_points: list[MeasurementPoint]
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        measurement_points = []
        for measurement_points_item_data in self.measurement_points:
            measurement_points_item = measurement_points_item_data.to_dict()
            measurement_points.append(measurement_points_item)

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "measurement_points": measurement_points,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.measurement_point import MeasurementPoint

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        measurement_points = []
        _measurement_points = d.pop("measurement_points")
        for measurement_points_item_data in _measurement_points:
            measurement_points_item = MeasurementPoint.from_dict(measurement_points_item_data)

            measurement_points.append(measurement_points_item)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        span_phase = cls(
            id=id,
            measurement_points=measurement_points,
            name=name,
        )

        span_phase.additional_properties = d
        return span_phase

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

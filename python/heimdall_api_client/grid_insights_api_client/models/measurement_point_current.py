from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.current_data_point import CurrentDataPoint


T = TypeVar("T", bound="MeasurementPointCurrent")


@_attrs_define
class MeasurementPointCurrent:
    """
    Attributes:
        measurement_point_id (UUID): The id of the measurement point. Example: 00000000-0000-0000-0000-000000000000.
        currents (list[CurrentDataPoint]): Current readings for this measurement point within the requested time range.
    """

    measurement_point_id: UUID
    currents: list[CurrentDataPoint]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measurement_point_id = str(self.measurement_point_id)

        currents = []
        for currents_item_data in self.currents:
            currents_item = currents_item_data.to_dict()
            currents.append(currents_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "measurement_point_id": measurement_point_id,
                "currents": currents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.current_data_point import CurrentDataPoint

        d = dict(src_dict)
        measurement_point_id = UUID(d.pop("measurement_point_id"))

        currents = []
        _currents = d.pop("currents")
        for currents_item_data in _currents:
            currents_item = CurrentDataPoint.from_dict(currents_item_data)

            currents.append(currents_item)

        measurement_point_current = cls(
            measurement_point_id=measurement_point_id,
            currents=currents,
        )

        measurement_point_current.additional_properties = d
        return measurement_point_current

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

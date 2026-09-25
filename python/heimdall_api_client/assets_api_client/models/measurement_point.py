from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MeasurementPoint")


@_attrs_define
class MeasurementPoint:
    """
    Attributes:
        id (UUID): Unique identifier of the measurement point. Example: 00000000-0000-0000-0000-000000000000.
        sub_conductor_number (int): The sub-conductor of the span phase that the measurement point sits on, from 1 up to
            the number of sub-conductors on the span. Example: 1.
        registered_timestamp (datetime.datetime): The timestamp when Heimdall Power registered the Neuron installation.
            Not necessarily when the Neuron was physically installed. Example: 2024-07-01 12:00:00.001000+00:00.
        unregistered_timestamp (datetime.datetime | None | Unset): The timestamp when the Neuron was uninstalled. Null
            while a Neuron is installed. Example: 2026-03-15 09:30:00+00:00.
    """

    id: UUID
    sub_conductor_number: int
    registered_timestamp: datetime.datetime
    unregistered_timestamp: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        sub_conductor_number = self.sub_conductor_number

        registered_timestamp = self.registered_timestamp.isoformat()

        unregistered_timestamp: None | str | Unset
        if isinstance(self.unregistered_timestamp, Unset):
            unregistered_timestamp = UNSET
        elif isinstance(self.unregistered_timestamp, datetime.datetime):
            unregistered_timestamp = self.unregistered_timestamp.isoformat()
        else:
            unregistered_timestamp = self.unregistered_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sub_conductor_number": sub_conductor_number,
                "registered_timestamp": registered_timestamp,
            }
        )
        if unregistered_timestamp is not UNSET:
            field_dict["unregistered_timestamp"] = unregistered_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        sub_conductor_number = d.pop("sub_conductor_number")

        registered_timestamp = isoparse(d.pop("registered_timestamp"))

        def _parse_unregistered_timestamp(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                unregistered_timestamp_type_0 = isoparse(data)

                return unregistered_timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        unregistered_timestamp = _parse_unregistered_timestamp(d.pop("unregistered_timestamp", UNSET))

        measurement_point = cls(
            id=id,
            sub_conductor_number=sub_conductor_number,
            registered_timestamp=registered_timestamp,
            unregistered_timestamp=unregistered_timestamp,
        )

        measurement_point.additional_properties = d
        return measurement_point

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

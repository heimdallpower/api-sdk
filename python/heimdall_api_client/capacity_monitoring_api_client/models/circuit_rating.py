from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime


T = TypeVar("T", bound="CircuitRating")


@_attrs_define
class CircuitRating:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the circuit rating was calculated. Example:
            2024-07-01T12:00:00.001Z.
        value (float): The minimum calculated ampacity (in amperes) at the given timestamp. Example: 375.4.
    """

    timestamp: datetime.datetime
    value: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        value = d.pop("value")

        circuit_rating = cls(
            timestamp=timestamp,
            value=value,
        )

        circuit_rating.additional_properties = d
        return circuit_rating

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

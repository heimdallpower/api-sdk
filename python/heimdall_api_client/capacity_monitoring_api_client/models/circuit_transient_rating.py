from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.circuit_transient_rating_value import CircuitTransientRatingValue


T = TypeVar("T", bound="CircuitTransientRating")


@_attrs_define
class CircuitTransientRating:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the circuit transient rating was calculated. Example:
            2024-07-01 12:00:00.001000+00:00.
        ratings (list[CircuitTransientRatingValue]): The circuit transient rating for each configured duration at the
            given timestamp. Ordered by `duration_minutes` ascending.
    """

    timestamp: datetime.datetime
    ratings: list[CircuitTransientRatingValue]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        ratings = []
        for ratings_item_data in self.ratings:
            ratings_item = ratings_item_data.to_dict()
            ratings.append(ratings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "ratings": ratings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_transient_rating_value import CircuitTransientRatingValue

        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        ratings = []
        _ratings = d.pop("ratings")
        for ratings_item_data in _ratings:
            ratings_item = CircuitTransientRatingValue.from_dict(ratings_item_data)

            ratings.append(ratings_item)

        circuit_transient_rating = cls(
            timestamp=timestamp,
            ratings=ratings,
        )

        circuit_transient_rating.additional_properties = d
        return circuit_transient_rating

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

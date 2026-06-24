from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.circuit_rating import CircuitRating


T = TypeVar("T", bound="CircuitRatings")


@_attrs_define
class CircuitRatings:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Circuit rating.
        unit (str): The unit of the values in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        circuit_ratings (list[CircuitRating]): List of circuit ratings within the requested time range.
    """

    metric: str
    unit: str
    circuit_ratings: list[CircuitRating]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        circuit_ratings = []
        for circuit_ratings_item_data in self.circuit_ratings:
            circuit_ratings_item = circuit_ratings_item_data.to_dict()
            circuit_ratings.append(circuit_ratings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "circuit_ratings": circuit_ratings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_rating import CircuitRating

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        circuit_ratings = []
        _circuit_ratings = d.pop("circuit_ratings")
        for circuit_ratings_item_data in _circuit_ratings:
            circuit_ratings_item = CircuitRating.from_dict(circuit_ratings_item_data)

            circuit_ratings.append(circuit_ratings_item)

        circuit_ratings = cls(
            metric=metric,
            unit=unit,
            circuit_ratings=circuit_ratings,
        )

        circuit_ratings.additional_properties = d
        return circuit_ratings

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

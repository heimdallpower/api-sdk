from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.circuit_transient_rating import CircuitTransientRating


T = TypeVar("T", bound="LatestCircuitTransientRating")


@_attrs_define
class LatestCircuitTransientRating:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Circuit transient rating.
        unit (str): The unit of the values in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        circuit_transient_rating (CircuitTransientRating):
    """

    metric: str
    unit: str
    circuit_transient_rating: CircuitTransientRating
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        circuit_transient_rating = self.circuit_transient_rating.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "circuit_transient_rating": circuit_transient_rating,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_transient_rating import CircuitTransientRating

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        circuit_transient_rating = CircuitTransientRating.from_dict(d.pop("circuit_transient_rating"))

        latest_circuit_transient_rating = cls(
            metric=metric,
            unit=unit,
            circuit_transient_rating=circuit_transient_rating,
        )

        latest_circuit_transient_rating.additional_properties = d
        return latest_circuit_transient_rating

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

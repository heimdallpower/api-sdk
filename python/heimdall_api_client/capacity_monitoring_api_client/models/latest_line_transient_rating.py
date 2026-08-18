from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_transient_rating import LineTransientRating


T = TypeVar("T", bound="LatestLineTransientRating")


@_attrs_define
class LatestLineTransientRating:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Line transient rating.
        unit (str): The unit of the values in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        line_transient_rating (LineTransientRating):
    """

    metric: str
    unit: str
    line_transient_rating: LineTransientRating
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        line_transient_rating = self.line_transient_rating.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "line_transient_rating": line_transient_rating,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_transient_rating import LineTransientRating

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        line_transient_rating = LineTransientRating.from_dict(d.pop("line_transient_rating"))

        latest_line_transient_rating = cls(
            metric=metric,
            unit=unit,
            line_transient_rating=line_transient_rating,
        )

        latest_line_transient_rating.additional_properties = d
        return latest_line_transient_rating

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

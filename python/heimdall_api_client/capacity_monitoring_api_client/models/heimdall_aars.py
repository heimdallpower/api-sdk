from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_aar import HeimdallAar


T = TypeVar("T", bound="HeimdallAars")


@_attrs_define
class HeimdallAars:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Heimdall AAR.
        unit (str): The unit of the values in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        heimdall_aars (list[HeimdallAar]): List of Heimdall AAR values within the requested time range. May be empty if
            no data exists for the period.
    """

    metric: str
    unit: str
    heimdall_aars: list[HeimdallAar]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        heimdall_aars = []
        for heimdall_aars_item_data in self.heimdall_aars:
            heimdall_aars_item = heimdall_aars_item_data.to_dict()
            heimdall_aars.append(heimdall_aars_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "heimdall_aars": heimdall_aars,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_aar import HeimdallAar

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        heimdall_aars = []
        _heimdall_aars = d.pop("heimdall_aars")
        for heimdall_aars_item_data in _heimdall_aars:
            heimdall_aars_item = HeimdallAar.from_dict(heimdall_aars_item_data)

            heimdall_aars.append(heimdall_aars_item)

        heimdall_aars = cls(
            metric=metric,
            unit=unit,
            heimdall_aars=heimdall_aars,
        )

        heimdall_aars.additional_properties = d
        return heimdall_aars

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

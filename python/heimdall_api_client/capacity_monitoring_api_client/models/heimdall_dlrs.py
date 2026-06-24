from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_dlr import HeimdallDlr


T = TypeVar("T", bound="HeimdallDlrs")


@_attrs_define
class HeimdallDlrs:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Heimdall DLR.
        unit (str): The unit of the values in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        heimdall_dlrs (list[HeimdallDlr]): List of Heimdall DLR values within the requested time range. May be empty if
            no data exists for the period.
    """

    metric: str
    unit: str
    heimdall_dlrs: list[HeimdallDlr]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        heimdall_dlrs = []
        for heimdall_dlrs_item_data in self.heimdall_dlrs:
            heimdall_dlrs_item = heimdall_dlrs_item_data.to_dict()
            heimdall_dlrs.append(heimdall_dlrs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "heimdall_dlrs": heimdall_dlrs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_dlr import HeimdallDlr

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        heimdall_dlrs = []
        _heimdall_dlrs = d.pop("heimdall_dlrs")
        for heimdall_dlrs_item_data in _heimdall_dlrs:
            heimdall_dlrs_item = HeimdallDlr.from_dict(heimdall_dlrs_item_data)

            heimdall_dlrs.append(heimdall_dlrs_item)

        heimdall_dlrs = cls(
            metric=metric,
            unit=unit,
            heimdall_dlrs=heimdall_dlrs,
        )

        heimdall_dlrs.additional_properties = d
        return heimdall_dlrs

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

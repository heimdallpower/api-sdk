from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_sag_and_clearances_sag_and_clearance import LineSagAndClearancesSagAndClearance


T = TypeVar("T", bound="LineSagAndClearances")


@_attrs_define
class LineSagAndClearances:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: SagAndClearance.
        unit (str): The unit of the values in the response. Example: Multiple (see measurements).
        sag_and_clearance (LineSagAndClearancesSagAndClearance): Sag and clearance measurements for the line over the
            requested time range, including the line-level maximum sag and minimum clearance values, as well as detailed
            measurements organized by spans and span phases.
    """

    metric: str
    unit: str
    sag_and_clearance: LineSagAndClearancesSagAndClearance
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        sag_and_clearance = self.sag_and_clearance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "sag_and_clearance": sag_and_clearance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_sag_and_clearances_sag_and_clearance import LineSagAndClearancesSagAndClearance

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        sag_and_clearance = LineSagAndClearancesSagAndClearance.from_dict(d.pop("sag_and_clearance"))

        line_sag_and_clearances = cls(
            metric=metric,
            unit=unit,
            sag_and_clearance=sag_and_clearance,
        )

        line_sag_and_clearances.additional_properties = d
        return line_sag_and_clearances

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

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_sag_and_clearance import LineSagAndClearance


T = TypeVar("T", bound="LatestSagAndClearance")


@_attrs_define
class LatestSagAndClearance:
    """
    Attributes:
        metric (str): The kind of data this response contains. Example: SagAndClearance.
        unit (str): The unit description for the response (multiple units across measurements).
        sag_and_clearance (LineSagAndClearance): The sag and clearance measurement.
    """

    metric: str
    unit: str
    sag_and_clearance: "LineSagAndClearance"
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
        from ..models.line_sag_and_clearance import LineSagAndClearance

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        sag_and_clearance = LineSagAndClearance.from_dict(d.pop("sag_and_clearance"))

        latest_sag_and_clearance = cls(
            metric=metric,
            unit=unit,
            sag_and_clearance=sag_and_clearance,
        )

        latest_sag_and_clearance.additional_properties = d
        return latest_sag_and_clearance

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

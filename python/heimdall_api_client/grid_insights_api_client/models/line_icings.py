from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_icings_icing import LineIcingsIcing


T = TypeVar("T", bound="LineIcings")


@_attrs_define
class LineIcings:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Icing.
        unit (str): The unit of the values in the response. Example: Multiple (see measurements).
        icing (LineIcingsIcing): Icing measurements for the line over the requested time range, organized by spans and
            span phases.
    """

    metric: str
    unit: str
    icing: LineIcingsIcing
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        icing = self.icing.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "icing": icing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_icings_icing import LineIcingsIcing

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        icing = LineIcingsIcing.from_dict(d.pop("icing"))

        line_icings = cls(
            metric=metric,
            unit=unit,
            icing=icing,
        )

        line_icings.additional_properties = d
        return line_icings

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

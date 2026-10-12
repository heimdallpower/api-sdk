from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_span_aar import HeimdallSpanAar


T = TypeVar("T", bound="HeimdallSpanAarSeries")


@_attrs_define
class HeimdallSpanAarSeries:
    """
    Attributes:
        span_id (UUID): The id of the span. Example: 00000000-0000-0000-0000-000000000000.
        heimdall_aars (list[HeimdallSpanAar]): Heimdall AAR values for this span within the requested time range,
            ordered by timestamp.
    """

    span_id: UUID
    heimdall_aars: list[HeimdallSpanAar]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_id = str(self.span_id)

        heimdall_aars = []
        for heimdall_aars_item_data in self.heimdall_aars:
            heimdall_aars_item = heimdall_aars_item_data.to_dict()
            heimdall_aars.append(heimdall_aars_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_id": span_id,
                "heimdall_aars": heimdall_aars,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_span_aar import HeimdallSpanAar

        d = dict(src_dict)
        span_id = UUID(d.pop("span_id"))

        heimdall_aars = []
        _heimdall_aars = d.pop("heimdall_aars")
        for heimdall_aars_item_data in _heimdall_aars:
            heimdall_aars_item = HeimdallSpanAar.from_dict(heimdall_aars_item_data)

            heimdall_aars.append(heimdall_aars_item)

        heimdall_span_aar_series = cls(
            span_id=span_id,
            heimdall_aars=heimdall_aars,
        )

        heimdall_span_aar_series.additional_properties = d
        return heimdall_span_aar_series

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

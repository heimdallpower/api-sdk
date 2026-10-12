from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_span_dlr import HeimdallSpanDlr


T = TypeVar("T", bound="HeimdallSpanDlrSeries")


@_attrs_define
class HeimdallSpanDlrSeries:
    """
    Attributes:
        span_id (UUID): The id of the span. Example: 00000000-0000-0000-0000-000000000000.
        heimdall_dlrs (list[HeimdallSpanDlr]): Heimdall DLR values for this span within the requested time range,
            ordered by timestamp.
    """

    span_id: UUID
    heimdall_dlrs: list[HeimdallSpanDlr]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_id = str(self.span_id)

        heimdall_dlrs = []
        for heimdall_dlrs_item_data in self.heimdall_dlrs:
            heimdall_dlrs_item = heimdall_dlrs_item_data.to_dict()
            heimdall_dlrs.append(heimdall_dlrs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_id": span_id,
                "heimdall_dlrs": heimdall_dlrs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_span_dlr import HeimdallSpanDlr

        d = dict(src_dict)
        span_id = UUID(d.pop("span_id"))

        heimdall_dlrs = []
        _heimdall_dlrs = d.pop("heimdall_dlrs")
        for heimdall_dlrs_item_data in _heimdall_dlrs:
            heimdall_dlrs_item = HeimdallSpanDlr.from_dict(heimdall_dlrs_item_data)

            heimdall_dlrs.append(heimdall_dlrs_item)

        heimdall_span_dlr_series = cls(
            span_id=span_id,
            heimdall_dlrs=heimdall_dlrs,
        )

        heimdall_span_dlr_series.additional_properties = d
        return heimdall_span_dlr_series

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

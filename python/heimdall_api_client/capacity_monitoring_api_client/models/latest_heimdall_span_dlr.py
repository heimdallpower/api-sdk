from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_span_dlr import HeimdallSpanDlr


T = TypeVar("T", bound="LatestHeimdallSpanDlr")


@_attrs_define
class LatestHeimdallSpanDlr:
    """
    Attributes:
        span_id (UUID): The id of the span. Example: 00000000-0000-0000-0000-000000000000.
        heimdall_dlr (HeimdallSpanDlr):
    """

    span_id: UUID
    heimdall_dlr: HeimdallSpanDlr
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_id = str(self.span_id)

        heimdall_dlr = self.heimdall_dlr.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_id": span_id,
                "heimdall_dlr": heimdall_dlr,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_span_dlr import HeimdallSpanDlr

        d = dict(src_dict)
        span_id = UUID(d.pop("span_id"))

        heimdall_dlr = HeimdallSpanDlr.from_dict(d.pop("heimdall_dlr"))

        latest_heimdall_span_dlr = cls(
            span_id=span_id,
            heimdall_dlr=heimdall_dlr,
        )

        latest_heimdall_span_dlr.additional_properties = d
        return latest_heimdall_span_dlr

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

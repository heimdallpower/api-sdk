from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.heimdall_span_aar import HeimdallSpanAar


T = TypeVar("T", bound="LatestHeimdallSpanAar")


@_attrs_define
class LatestHeimdallSpanAar:
    """
    Attributes:
        span_id (UUID): The id of the span. Example: 00000000-0000-0000-0000-000000000000.
        heimdall_aar (HeimdallSpanAar):
    """

    span_id: UUID
    heimdall_aar: HeimdallSpanAar
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_id = str(self.span_id)

        heimdall_aar = self.heimdall_aar.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_id": span_id,
                "heimdall_aar": heimdall_aar,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_span_aar import HeimdallSpanAar

        d = dict(src_dict)
        span_id = UUID(d.pop("span_id"))

        heimdall_aar = HeimdallSpanAar.from_dict(d.pop("heimdall_aar"))

        latest_heimdall_span_aar = cls(
            span_id=span_id,
            heimdall_aar=heimdall_aar,
        )

        latest_heimdall_span_aar.additional_properties = d
        return latest_heimdall_span_aar

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

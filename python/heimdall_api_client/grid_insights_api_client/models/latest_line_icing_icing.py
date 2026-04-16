from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.max_icing import MaxIcing
    from ..models.span_icing import SpanIcing


T = TypeVar("T", bound="LatestLineIcingIcing")


@_attrs_define
class LatestLineIcingIcing:
    """Icing measurements for the line organized by spans and span phases.

    Attributes:
        spans (list[SpanIcing]): List of spans on the line with their icing data.
        max_ (MaxIcing | Unset):
    """

    spans: list[SpanIcing]
    max_: MaxIcing | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)

        max_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.max_, Unset):
            max_ = self.max_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "spans": spans,
            }
        )
        if max_ is not UNSET:
            field_dict["max"] = max_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.max_icing import MaxIcing
        from ..models.span_icing import SpanIcing

        d = dict(src_dict)
        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:
            spans_item = SpanIcing.from_dict(spans_item_data)

            spans.append(spans_item)

        _max_ = d.pop("max", UNSET)
        max_: MaxIcing | Unset
        if isinstance(_max_, Unset):
            max_ = UNSET
        else:
            max_ = MaxIcing.from_dict(_max_)

        latest_line_icing_icing = cls(
            spans=spans,
            max_=max_,
        )

        latest_line_icing_icing.additional_properties = d
        return latest_line_icing_icing

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

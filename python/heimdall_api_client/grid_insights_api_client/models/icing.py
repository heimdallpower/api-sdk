from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.max_icing import MaxIcing
    from ..models.span_icing import SpanIcing


T = TypeVar("T", bound="Icing")


@_attrs_define
class Icing:
    """
    Attributes:
        max_ (MaxIcing): The maximum icing data across all span phases on the line.
        spans (list[SpanIcing]): List of spans on the line with their icing data.
    """

    max_: "MaxIcing"
    spans: list["SpanIcing"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_ = self.max_.to_dict()

        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max": max_,
                "spans": spans,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.max_icing import MaxIcing
        from ..models.span_icing import SpanIcing

        d = dict(src_dict)
        max_ = MaxIcing.from_dict(d.pop("max"))

        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:
            spans_item = SpanIcing.from_dict(spans_item_data)
            spans.append(spans_item)

        icing = cls(
            max_=max_,
            spans=spans,
        )

        icing.additional_properties = d
        return icing

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

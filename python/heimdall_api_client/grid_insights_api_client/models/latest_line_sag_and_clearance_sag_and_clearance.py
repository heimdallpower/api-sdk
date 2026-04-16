from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.latest_line_sag_and_clearance_sag_and_clearance_max_sag import (
        LatestLineSagAndClearanceSagAndClearanceMaxSag,
    )
    from ..models.latest_line_sag_and_clearance_sag_and_clearance_min_clearance_type_1 import (
        LatestLineSagAndClearanceSagAndClearanceMinClearanceType1,
    )
    from ..models.span_sag_and_clearance import SpanSagAndClearance


T = TypeVar("T", bound="LatestLineSagAndClearanceSagAndClearance")


@_attrs_define
class LatestLineSagAndClearanceSagAndClearance:
    """Sag and clearance measurements for the line, including the line-level maximum sag and minimum clearance values, as
    well as detailed measurements organized by spans and span phases.

        Attributes:
            max_sag (LatestLineSagAndClearanceSagAndClearanceMaxSag): The span phase with the maximum sag across all span
                phases on the line.
            spans (list[SpanSagAndClearance]): List of spans on the line with their sag and clearance data.
            min_clearance (LatestLineSagAndClearanceSagAndClearanceMinClearanceType1 | None | Unset): The span phase with
                the minimum clearance across all span phases on the line. Null if no span phase has clearance data.
    """

    max_sag: LatestLineSagAndClearanceSagAndClearanceMaxSag
    spans: list[SpanSagAndClearance]
    min_clearance: LatestLineSagAndClearanceSagAndClearanceMinClearanceType1 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.latest_line_sag_and_clearance_sag_and_clearance_min_clearance_type_1 import (
            LatestLineSagAndClearanceSagAndClearanceMinClearanceType1,
        )

        max_sag = self.max_sag.to_dict()

        spans = []
        for spans_item_data in self.spans:
            spans_item = spans_item_data.to_dict()
            spans.append(spans_item)

        min_clearance: dict[str, Any] | None | Unset
        if isinstance(self.min_clearance, Unset):
            min_clearance = UNSET
        elif isinstance(self.min_clearance, LatestLineSagAndClearanceSagAndClearanceMinClearanceType1):
            min_clearance = self.min_clearance.to_dict()
        else:
            min_clearance = self.min_clearance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_sag": max_sag,
                "spans": spans,
            }
        )
        if min_clearance is not UNSET:
            field_dict["min_clearance"] = min_clearance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_line_sag_and_clearance_sag_and_clearance_max_sag import (
            LatestLineSagAndClearanceSagAndClearanceMaxSag,
        )
        from ..models.latest_line_sag_and_clearance_sag_and_clearance_min_clearance_type_1 import (
            LatestLineSagAndClearanceSagAndClearanceMinClearanceType1,
        )
        from ..models.span_sag_and_clearance import SpanSagAndClearance

        d = dict(src_dict)
        max_sag = LatestLineSagAndClearanceSagAndClearanceMaxSag.from_dict(d.pop("max_sag"))

        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:
            spans_item = SpanSagAndClearance.from_dict(spans_item_data)

            spans.append(spans_item)

        def _parse_min_clearance(
            data: object,
        ) -> LatestLineSagAndClearanceSagAndClearanceMinClearanceType1 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                min_clearance_type_1 = LatestLineSagAndClearanceSagAndClearanceMinClearanceType1.from_dict(data)

                return min_clearance_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LatestLineSagAndClearanceSagAndClearanceMinClearanceType1 | None | Unset, data)

        min_clearance = _parse_min_clearance(d.pop("min_clearance", UNSET))

        latest_line_sag_and_clearance_sag_and_clearance = cls(
            max_sag=max_sag,
            spans=spans,
            min_clearance=min_clearance,
        )

        latest_line_sag_and_clearance_sag_and_clearance.additional_properties = d
        return latest_line_sag_and_clearance_sag_and_clearance

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

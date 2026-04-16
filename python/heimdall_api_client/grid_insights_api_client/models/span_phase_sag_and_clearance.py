from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.span_phase_sag_and_clearance_clearance_type_1 import SpanPhaseSagAndClearanceClearanceType1
    from ..models.span_phase_sag_and_clearance_sag import SpanPhaseSagAndClearanceSag


T = TypeVar("T", bound="SpanPhaseSagAndClearance")


@_attrs_define
class SpanPhaseSagAndClearance:
    """
    Attributes:
        span_phase_id (UUID): The id of the span phase. Example: 00000000-0000-0000-0000-000000000000.
        timestamp (datetime.datetime): Time (in UTC) when the sag and clearance measurements were calculated for this
            specific span phase. Example: 2026-03-31 11:11:45.387000+00:00.
        sag (SpanPhaseSagAndClearanceSag):
        clearance (None | SpanPhaseSagAndClearanceClearanceType1 | Unset):
    """

    span_phase_id: UUID
    timestamp: datetime.datetime
    sag: SpanPhaseSagAndClearanceSag
    clearance: None | SpanPhaseSagAndClearanceClearanceType1 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.span_phase_sag_and_clearance_clearance_type_1 import SpanPhaseSagAndClearanceClearanceType1

        span_phase_id = str(self.span_phase_id)

        timestamp = self.timestamp.isoformat()

        sag = self.sag.to_dict()

        clearance: dict[str, Any] | None | Unset
        if isinstance(self.clearance, Unset):
            clearance = UNSET
        elif isinstance(self.clearance, SpanPhaseSagAndClearanceClearanceType1):
            clearance = self.clearance.to_dict()
        else:
            clearance = self.clearance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_phase_id": span_phase_id,
                "timestamp": timestamp,
                "sag": sag,
            }
        )
        if clearance is not UNSET:
            field_dict["clearance"] = clearance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_phase_sag_and_clearance_clearance_type_1 import SpanPhaseSagAndClearanceClearanceType1
        from ..models.span_phase_sag_and_clearance_sag import SpanPhaseSagAndClearanceSag

        d = dict(src_dict)
        span_phase_id = UUID(d.pop("span_phase_id"))

        timestamp = isoparse(d.pop("timestamp"))

        sag = SpanPhaseSagAndClearanceSag.from_dict(d.pop("sag"))

        def _parse_clearance(data: object) -> None | SpanPhaseSagAndClearanceClearanceType1 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                clearance_type_1 = SpanPhaseSagAndClearanceClearanceType1.from_dict(data)

                return clearance_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SpanPhaseSagAndClearanceClearanceType1 | Unset, data)

        clearance = _parse_clearance(d.pop("clearance", UNSET))

        span_phase_sag_and_clearance = cls(
            span_phase_id=span_phase_id,
            timestamp=timestamp,
            sag=sag,
            clearance=clearance,
        )

        span_phase_sag_and_clearance.additional_properties = d
        return span_phase_sag_and_clearance

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

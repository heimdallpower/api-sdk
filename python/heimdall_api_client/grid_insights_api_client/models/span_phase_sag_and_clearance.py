from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING, Optional

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from dateutil.parser import isoparse
import datetime
from uuid import UUID

if TYPE_CHECKING:
    from ..models.measurement_result import MeasurementResult


T = TypeVar("T", bound="SpanPhaseSagAndClearance")


@_attrs_define
class SpanPhaseSagAndClearance:
    """
    Attributes:
        span_phase_id (UUID): The id of the span phase the measurement belongs to.
        timestamp (datetime.datetime): Time (UTC) when the measurements were calculated for the span phase.
        sag (MeasurementResult): The maximum vertical deflection of the conductor from the straight line between its two
            support points.
        clearance (Optional[MeasurementResult]): The vertical distance between the conductor and the ground or objects
            below.
    """

    span_phase_id: UUID
    timestamp: datetime.datetime
    sag: "MeasurementResult"
    clearance: Optional["MeasurementResult"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_phase_id = str(self.span_phase_id)

        timestamp = self.timestamp.isoformat()

        sag = self.sag.to_dict()

        clearance = self.clearance.to_dict() if self.clearance is not None else None

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_phase_id": span_phase_id,
                "timestamp": timestamp,
                "sag": sag,
                "clearance": clearance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.measurement_result import MeasurementResult

        d = dict(src_dict)
        span_phase_id = UUID(d.pop("span_phase_id"))

        timestamp = isoparse(d.pop("timestamp"))

        sag = MeasurementResult.from_dict(d.pop("sag"))

        _clearance = d.pop("clearance", None)
        clearance = MeasurementResult.from_dict(_clearance) if _clearance is not None else None

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

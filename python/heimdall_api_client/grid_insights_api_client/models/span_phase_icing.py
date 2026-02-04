from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from dateutil.parser import isoparse
import datetime
from uuid import UUID

if TYPE_CHECKING:
    from ..models.measurement_result import MeasurementResult


T = TypeVar("T", bound="SpanPhaseIcing")


@_attrs_define
class SpanPhaseIcing:
    """
    Attributes:
        span_phase_id (UUID): The id of the span phase the measurement belongs to.
        timestamp (datetime.datetime): Time (UTC) when the icing measurements were calculated for the span phase.
        ice_weight (MeasurementResult): The mass of ice accumulated on the conductor.
        tension (MeasurementResult): The mechanical tension force in the conductor.
        tension_percentage_of_break_strength (MeasurementResult): Safety-critical metric showing how close the conductor
            is to its breaking point.
    """

    span_phase_id: UUID
    timestamp: datetime.datetime
    ice_weight: "MeasurementResult"
    tension: "MeasurementResult"
    tension_percentage_of_break_strength: "MeasurementResult"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_phase_id = str(self.span_phase_id)

        timestamp = self.timestamp.isoformat()

        ice_weight = self.ice_weight.to_dict()

        tension = self.tension.to_dict()

        tension_percentage_of_break_strength = self.tension_percentage_of_break_strength.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_phase_id": span_phase_id,
                "timestamp": timestamp,
                "ice_weight": ice_weight,
                "tension": tension,
                "tension_percentage_of_break_strength": tension_percentage_of_break_strength,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.measurement_result import MeasurementResult

        d = dict(src_dict)
        span_phase_id = UUID(d.pop("span_phase_id"))

        timestamp = isoparse(d.pop("timestamp"))

        ice_weight = MeasurementResult.from_dict(d.pop("ice_weight"))

        tension = MeasurementResult.from_dict(d.pop("tension"))

        tension_percentage_of_break_strength = MeasurementResult.from_dict(d.pop("tension_percentage_of_break_strength"))

        span_phase_icing = cls(
            span_phase_id=span_phase_id,
            timestamp=timestamp,
            ice_weight=ice_weight,
            tension=tension,
            tension_percentage_of_break_strength=tension_percentage_of_break_strength,
        )

        span_phase_icing.additional_properties = d
        return span_phase_icing

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

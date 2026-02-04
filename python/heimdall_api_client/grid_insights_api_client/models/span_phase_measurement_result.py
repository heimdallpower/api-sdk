from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from dateutil.parser import isoparse
import datetime
from uuid import UUID


T = TypeVar("T", bound="SpanPhaseMeasurementResult")


@_attrs_define
class SpanPhaseMeasurementResult:
    """
    Attributes:
        timestamp (datetime.datetime): Time (UTC) when the icing measurements were calculated for the span phase.
        span_phase_id (UUID): The id of the span phase the measurement belongs to.
        value (float): The numerical value of the measurement.
        unit (str): The unit of the measurement value.
    """

    timestamp: datetime.datetime
    span_phase_id: UUID
    value: float
    unit: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        span_phase_id = str(self.span_phase_id)

        value = self.value

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "span_phase_id": span_phase_id,
                "value": value,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        span_phase_id = UUID(d.pop("span_phase_id"))

        value = d.pop("value")

        unit = d.pop("unit")

        span_phase_measurement_result = cls(
            timestamp=timestamp,
            span_phase_id=span_phase_id,
            value=value,
            unit=unit,
        )

        span_phase_measurement_result.additional_properties = d
        return span_phase_measurement_result

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

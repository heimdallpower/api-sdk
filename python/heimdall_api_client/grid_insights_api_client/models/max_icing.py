from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.span_phase_measurement_result import SpanPhaseMeasurementResult


T = TypeVar("T", bound="MaxIcing")


@_attrs_define
class MaxIcing:
    """
    Attributes:
        ice_weight (SpanPhaseMeasurementResult): The maximum mass of ice accumulated on the conductor.
        tension (SpanPhaseMeasurementResult): The maximum mechanical tension force in the conductor.
        tension_percentage_of_break_strength (SpanPhaseMeasurementResult): Maximum safety-critical metric showing how
            close the conductor is to its breaking point.
    """

    ice_weight: "SpanPhaseMeasurementResult"
    tension: "SpanPhaseMeasurementResult"
    tension_percentage_of_break_strength: "SpanPhaseMeasurementResult"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ice_weight = self.ice_weight.to_dict()

        tension = self.tension.to_dict()

        tension_percentage_of_break_strength = self.tension_percentage_of_break_strength.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ice_weight": ice_weight,
                "tension": tension,
                "tension_percentage_of_break_strength": tension_percentage_of_break_strength,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_phase_measurement_result import SpanPhaseMeasurementResult

        d = dict(src_dict)
        ice_weight = SpanPhaseMeasurementResult.from_dict(d.pop("ice_weight"))

        tension = SpanPhaseMeasurementResult.from_dict(d.pop("tension"))

        tension_percentage_of_break_strength = SpanPhaseMeasurementResult.from_dict(
            d.pop("tension_percentage_of_break_strength")
        )

        max_icing = cls(
            ice_weight=ice_weight,
            tension=tension,
            tension_percentage_of_break_strength=tension_percentage_of_break_strength,
        )

        max_icing.additional_properties = d
        return max_icing

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

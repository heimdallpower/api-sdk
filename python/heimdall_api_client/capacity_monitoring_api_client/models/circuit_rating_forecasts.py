from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
    from ..models.predicted_circuit_rating_forecast import PredictedCircuitRatingForecast


T = TypeVar("T", bound="CircuitRatingForecasts")


@_attrs_define
class CircuitRatingForecasts:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Circuit rating forecast.
        unit (str): The unit of the values in the response. Example: Ampere.
        updated_timestamp (datetime.datetime): The timestamp when the forecasts were last updated. Example:
            2024-07-01T12:00:00.001Z.
        circuit_rating_forecasts (list['PredictedCircuitRatingForecast']): The forecasts for a 1 hour interval starting
            from the `updated_timestamp`. The predicted forecasts includes different percentages of confidence.
    """

    metric: str
    unit: str
    updated_timestamp: datetime.datetime
    circuit_rating_forecasts: list["PredictedCircuitRatingForecast"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        updated_timestamp = self.updated_timestamp.isoformat()

        circuit_rating_forecasts = []
        for circuit_rating_forecasts_item_data in self.circuit_rating_forecasts:
            circuit_rating_forecasts_item = circuit_rating_forecasts_item_data.to_dict()
            circuit_rating_forecasts.append(circuit_rating_forecasts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "updated_timestamp": updated_timestamp,
                "circuit_rating_forecasts": circuit_rating_forecasts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.predicted_circuit_rating_forecast import PredictedCircuitRatingForecast

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        updated_timestamp = isoparse(d.pop("updated_timestamp"))

        circuit_rating_forecasts = []
        _circuit_rating_forecasts = d.pop("circuit_rating_forecasts")
        for circuit_rating_forecasts_item_data in _circuit_rating_forecasts:
            circuit_rating_forecasts_item = PredictedCircuitRatingForecast.from_dict(circuit_rating_forecasts_item_data)

            circuit_rating_forecasts.append(circuit_rating_forecasts_item)

        circuit_rating_forecasts = cls(
            metric=metric,
            unit=unit,
            updated_timestamp=updated_timestamp,
            circuit_rating_forecasts=circuit_rating_forecasts,
        )

        circuit_rating_forecasts.additional_properties = d
        return circuit_rating_forecasts

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

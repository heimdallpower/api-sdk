from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.icing_forecast_data_point import IcingForecastDataPoint


T = TypeVar("T", bound="SpanPhaseIcingForecast")


@_attrs_define
class SpanPhaseIcingForecast:
    """
    Attributes:
        span_phase_id (UUID): The id of the span phase. Example: 00000000-0000-0000-0000-000000000000.
        forecast (list[IcingForecastDataPoint]): Forecasted icing data points for this span phase. Covers 72 hours in
            30-minute intervals (144 data points).
    """

    span_phase_id: UUID
    forecast: list[IcingForecastDataPoint]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span_phase_id = str(self.span_phase_id)

        forecast = []
        for forecast_item_data in self.forecast:
            forecast_item = forecast_item_data.to_dict()
            forecast.append(forecast_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span_phase_id": span_phase_id,
                "forecast": forecast,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.icing_forecast_data_point import IcingForecastDataPoint

        d = dict(src_dict)
        span_phase_id = UUID(d.pop("span_phase_id"))

        forecast = []
        _forecast = d.pop("forecast")
        for forecast_item_data in _forecast:
            forecast_item = IcingForecastDataPoint.from_dict(forecast_item_data)

            forecast.append(forecast_item)

        span_phase_icing_forecast = cls(
            span_phase_id=span_phase_id,
            forecast=forecast,
        )

        span_phase_icing_forecast.additional_properties = d
        return span_phase_icing_forecast

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

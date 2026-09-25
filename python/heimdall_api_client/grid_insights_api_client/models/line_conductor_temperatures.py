from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conductor_temperature_values import ConductorTemperatureValues
    from ..models.span_conductor_temperature import SpanConductorTemperature


T = TypeVar("T", bound="LineConductorTemperatures")


@_attrs_define
class LineConductorTemperatures:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Conductor temperature.
        unit (str): The unit of the values in the response. Example: C.
        conductor_temperatures (list[ConductorTemperatureValues]): List of conductor temperature measurements within the
            requested time range. May be empty if no data exists for the period.
        measurement_point_temperatures (list[SpanConductorTemperature] | None | Unset): Per-measurement-point breakdown
            of conductor temperature over the requested time range, organized by span and span phase. Only present when
            `include=measurement_points` is set on the request; otherwise `null`.
    """

    metric: str
    unit: str
    conductor_temperatures: list[ConductorTemperatureValues]
    measurement_point_temperatures: list[SpanConductorTemperature] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        conductor_temperatures = []
        for conductor_temperatures_item_data in self.conductor_temperatures:
            conductor_temperatures_item = conductor_temperatures_item_data.to_dict()
            conductor_temperatures.append(conductor_temperatures_item)

        measurement_point_temperatures: list[dict[str, Any]] | None | Unset
        if isinstance(self.measurement_point_temperatures, Unset):
            measurement_point_temperatures = UNSET
        elif isinstance(self.measurement_point_temperatures, list):
            measurement_point_temperatures = []
            for measurement_point_temperatures_type_0_item_data in self.measurement_point_temperatures:
                measurement_point_temperatures_type_0_item = measurement_point_temperatures_type_0_item_data.to_dict()
                measurement_point_temperatures.append(measurement_point_temperatures_type_0_item)

        else:
            measurement_point_temperatures = self.measurement_point_temperatures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "conductor_temperatures": conductor_temperatures,
            }
        )
        if measurement_point_temperatures is not UNSET:
            field_dict["measurement_point_temperatures"] = measurement_point_temperatures

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conductor_temperature_values import ConductorTemperatureValues
        from ..models.span_conductor_temperature import SpanConductorTemperature

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        conductor_temperatures = []
        _conductor_temperatures = d.pop("conductor_temperatures")
        for conductor_temperatures_item_data in _conductor_temperatures:
            conductor_temperatures_item = ConductorTemperatureValues.from_dict(conductor_temperatures_item_data)

            conductor_temperatures.append(conductor_temperatures_item)

        def _parse_measurement_point_temperatures(data: object) -> list[SpanConductorTemperature] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                measurement_point_temperatures_type_0 = []
                _measurement_point_temperatures_type_0 = data
                for measurement_point_temperatures_type_0_item_data in _measurement_point_temperatures_type_0:
                    measurement_point_temperatures_type_0_item = SpanConductorTemperature.from_dict(
                        measurement_point_temperatures_type_0_item_data
                    )

                    measurement_point_temperatures_type_0.append(measurement_point_temperatures_type_0_item)

                return measurement_point_temperatures_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SpanConductorTemperature] | None | Unset, data)

        measurement_point_temperatures = _parse_measurement_point_temperatures(
            d.pop("measurement_point_temperatures", UNSET)
        )

        line_conductor_temperatures = cls(
            metric=metric,
            unit=unit,
            conductor_temperatures=conductor_temperatures,
            measurement_point_temperatures=measurement_point_temperatures,
        )

        line_conductor_temperatures.additional_properties = d
        return line_conductor_temperatures

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

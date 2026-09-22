from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.line_current import LineCurrent
    from ..models.span_current import SpanCurrent


T = TypeVar("T", bound="LineCurrents")


@_attrs_define
class LineCurrents:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Current.
        unit (str): The unit of the values in the response. Example: Ampere.
        currents (list[LineCurrent]): List of current measurements within the requested time range. May be empty if no
            data exists for the period.
        measurement_point_currents (list[SpanCurrent] | None | Unset): Per-measurement-point breakdown of current over
            the requested time range, organized by span and span phase. Only present when `include=measurement_points` is
            set on the request; otherwise `null`.
    """

    metric: str
    unit: str
    currents: list[LineCurrent]
    measurement_point_currents: list[SpanCurrent] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        currents = []
        for currents_item_data in self.currents:
            currents_item = currents_item_data.to_dict()
            currents.append(currents_item)

        measurement_point_currents: list[dict[str, Any]] | None | Unset
        if isinstance(self.measurement_point_currents, Unset):
            measurement_point_currents = UNSET
        elif isinstance(self.measurement_point_currents, list):
            measurement_point_currents = []
            for measurement_point_currents_type_0_item_data in self.measurement_point_currents:
                measurement_point_currents_type_0_item = measurement_point_currents_type_0_item_data.to_dict()
                measurement_point_currents.append(measurement_point_currents_type_0_item)

        else:
            measurement_point_currents = self.measurement_point_currents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "currents": currents,
            }
        )
        if measurement_point_currents is not UNSET:
            field_dict["measurement_point_currents"] = measurement_point_currents

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_current import LineCurrent
        from ..models.span_current import SpanCurrent

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        currents = []
        _currents = d.pop("currents")
        for currents_item_data in _currents:
            currents_item = LineCurrent.from_dict(currents_item_data)

            currents.append(currents_item)

        def _parse_measurement_point_currents(data: object) -> list[SpanCurrent] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                measurement_point_currents_type_0 = []
                _measurement_point_currents_type_0 = data
                for measurement_point_currents_type_0_item_data in _measurement_point_currents_type_0:
                    measurement_point_currents_type_0_item = SpanCurrent.from_dict(
                        measurement_point_currents_type_0_item_data
                    )

                    measurement_point_currents_type_0.append(measurement_point_currents_type_0_item)

                return measurement_point_currents_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SpanCurrent] | None | Unset, data)

        measurement_point_currents = _parse_measurement_point_currents(d.pop("measurement_point_currents", UNSET))

        line_currents = cls(
            metric=metric,
            unit=unit,
            currents=currents,
            measurement_point_currents=measurement_point_currents,
        )

        line_currents.additional_properties = d
        return line_currents

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

from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.icing_forecast_data_point_ice_weight import IcingForecastDataPointIceWeight


T = TypeVar("T", bound="IcingForecastDataPoint")


@_attrs_define
class IcingForecastDataPoint:
    """
    Attributes:
        timestamp (datetime.datetime): Time (UTC) for this forecast data point. Example: 2024-01-15 08:33:00+00:00.
        ice_weight (IcingForecastDataPointIceWeight):
    """

    timestamp: datetime.datetime
    ice_weight: IcingForecastDataPointIceWeight
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        ice_weight = self.ice_weight.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "ice_weight": ice_weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.icing_forecast_data_point_ice_weight import IcingForecastDataPointIceWeight

        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        ice_weight = IcingForecastDataPointIceWeight.from_dict(d.pop("ice_weight"))

        icing_forecast_data_point = cls(
            timestamp=timestamp,
            ice_weight=ice_weight,
        )

        icing_forecast_data_point.additional_properties = d
        return icing_forecast_data_point

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

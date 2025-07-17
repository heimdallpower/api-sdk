from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
  from ..models.predicted_forecast import PredictedForecast





T = TypeVar("T", bound="HeimdallAarForecasts")



@_attrs_define
class HeimdallAarForecasts:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Heimdall AAR forecast.
            unit (str): The unit of the values in the response. Example: Ampere.
            updated_timestamp (datetime.datetime): The timestamp when the forecasts were last updated. Example:
                2024-07-01T12:00:00.001Z.
            aar_forecasts (list['PredictedForecast']): The forecasts for a 1 hour interval starting from the
                `updated_timestamp`. The predicted forecasts includes different percentages of confidence.
     """

    metric: str
    unit: str
    updated_timestamp: datetime.datetime
    aar_forecasts: list['PredictedForecast']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        updated_timestamp = self.updated_timestamp.isoformat()

        aar_forecasts = []
        for aar_forecasts_item_data in self.aar_forecasts:
            aar_forecasts_item = aar_forecasts_item_data.to_dict()
            aar_forecasts.append(aar_forecasts_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "updated_timestamp": updated_timestamp,
            "aar_forecasts": aar_forecasts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.predicted_forecast import PredictedForecast
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        updated_timestamp = isoparse(d.pop("updated_timestamp"))




        aar_forecasts = []
        _aar_forecasts = d.pop("aar_forecasts")
        for aar_forecasts_item_data in (_aar_forecasts):
            aar_forecasts_item = PredictedForecast.from_dict(aar_forecasts_item_data)



            aar_forecasts.append(aar_forecasts_item)


        heimdall_aar_forecasts = cls(
            metric=metric,
            unit=unit,
            updated_timestamp=updated_timestamp,
            aar_forecasts=aar_forecasts,
        )


        heimdall_aar_forecasts.additional_properties = d
        return heimdall_aar_forecasts

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

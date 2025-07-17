from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
  from ..models.predicted_forecast import PredictedForecast





T = TypeVar("T", bound="HeimdallDlrForecasts")



@_attrs_define
class HeimdallDlrForecasts:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Heimdall DLR forecast.
            unit (str): The unit of the values in the response. Example: Ampere.
            updated_timestamp (datetime.datetime): The timestamp when the forecasts were last updated. Example:
                2024-07-01T12:00:00.001Z.
            dlr_forecasts (list['PredictedForecast']): The forecasts for a 1 hour interval starting from the
                `updated_timestamp`. The predicted forecasts includes different percentages of confidence.
     """

    metric: str
    unit: str
    updated_timestamp: datetime.datetime
    dlr_forecasts: list['PredictedForecast']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        updated_timestamp = self.updated_timestamp.isoformat()

        dlr_forecasts = []
        for dlr_forecasts_item_data in self.dlr_forecasts:
            dlr_forecasts_item = dlr_forecasts_item_data.to_dict()
            dlr_forecasts.append(dlr_forecasts_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "updated_timestamp": updated_timestamp,
            "dlr_forecasts": dlr_forecasts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.predicted_forecast import PredictedForecast
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        updated_timestamp = isoparse(d.pop("updated_timestamp"))




        dlr_forecasts = []
        _dlr_forecasts = d.pop("dlr_forecasts")
        for dlr_forecasts_item_data in (_dlr_forecasts):
            dlr_forecasts_item = PredictedForecast.from_dict(dlr_forecasts_item_data)



            dlr_forecasts.append(dlr_forecasts_item)


        heimdall_dlr_forecasts = cls(
            metric=metric,
            unit=unit,
            updated_timestamp=updated_timestamp,
            dlr_forecasts=dlr_forecasts,
        )


        heimdall_dlr_forecasts.additional_properties = d
        return heimdall_dlr_forecasts

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

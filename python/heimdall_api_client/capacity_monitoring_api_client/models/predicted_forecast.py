from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
  from ..models.probabilistic_line_ampacity import ProbabilisticLineAmpacity





T = TypeVar("T", bound="PredictedForecast")



@_attrs_define
class PredictedForecast:
    """ 
        Attributes:
            timestamp (datetime.datetime): Timestamp for the predicted forecast. Example: 2024-07-01T12:00:00.001Z.
            prediction (ProbabilisticLineAmpacity):
            p80 (ProbabilisticLineAmpacity):
            p90 (ProbabilisticLineAmpacity):
            p95 (ProbabilisticLineAmpacity):
            p99 (ProbabilisticLineAmpacity):
     """

    timestamp: datetime.datetime
    prediction: 'ProbabilisticLineAmpacity'
    p80: 'ProbabilisticLineAmpacity'
    p90: 'ProbabilisticLineAmpacity'
    p95: 'ProbabilisticLineAmpacity'
    p99: 'ProbabilisticLineAmpacity'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        prediction = self.prediction.to_dict()

        p80 = self.p80.to_dict()

        p90 = self.p90.to_dict()

        p95 = self.p95.to_dict()

        p99 = self.p99.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timestamp": timestamp,
            "prediction": prediction,
            "p80": p80,
            "p90": p90,
            "p95": p95,
            "p99": p99,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.probabilistic_line_ampacity import ProbabilisticLineAmpacity
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))




        prediction = ProbabilisticLineAmpacity.from_dict(d.pop("prediction"))




        p80 = ProbabilisticLineAmpacity.from_dict(d.pop("p80"))




        p90 = ProbabilisticLineAmpacity.from_dict(d.pop("p90"))




        p95 = ProbabilisticLineAmpacity.from_dict(d.pop("p95"))




        p99 = ProbabilisticLineAmpacity.from_dict(d.pop("p99"))




        predicted_forecast = cls(
            timestamp=timestamp,
            prediction=prediction,
            p80=p80,
            p90=p90,
            p95=p95,
            p99=p99,
        )


        predicted_forecast.additional_properties = d
        return predicted_forecast

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

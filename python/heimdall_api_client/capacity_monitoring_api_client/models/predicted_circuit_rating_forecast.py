from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.probabilistic_circuit_rating_ampacity import ProbabilisticCircuitRatingAmpacity





T = TypeVar("T", bound="PredictedCircuitRatingForecast")



@_attrs_define
class PredictedCircuitRatingForecast:
    """ 
        Attributes:
            timestamp (datetime.datetime): Timestamp for the predicted forecast. Example: 2024-07-01T12:00:00.001Z.
            prediction (ProbabilisticCircuitRatingAmpacity):
            p80 (ProbabilisticCircuitRatingAmpacity):
            p90 (ProbabilisticCircuitRatingAmpacity):
            p95 (ProbabilisticCircuitRatingAmpacity):
            p99 (ProbabilisticCircuitRatingAmpacity):
     """

    timestamp: datetime.datetime
    prediction: 'ProbabilisticCircuitRatingAmpacity'
    p80: 'ProbabilisticCircuitRatingAmpacity'
    p90: 'ProbabilisticCircuitRatingAmpacity'
    p95: 'ProbabilisticCircuitRatingAmpacity'
    p99: 'ProbabilisticCircuitRatingAmpacity'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.probabilistic_circuit_rating_ampacity import ProbabilisticCircuitRatingAmpacity
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
        from ..models.probabilistic_circuit_rating_ampacity import ProbabilisticCircuitRatingAmpacity
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))




        prediction = ProbabilisticCircuitRatingAmpacity.from_dict(d.pop("prediction"))




        p80 = ProbabilisticCircuitRatingAmpacity.from_dict(d.pop("p80"))




        p90 = ProbabilisticCircuitRatingAmpacity.from_dict(d.pop("p90"))




        p95 = ProbabilisticCircuitRatingAmpacity.from_dict(d.pop("p95"))




        p99 = ProbabilisticCircuitRatingAmpacity.from_dict(d.pop("p99"))




        predicted_circuit_rating_forecast = cls(
            timestamp=timestamp,
            prediction=prediction,
            p80=p80,
            p90=p90,
            p95=p95,
            p99=p99,
        )


        predicted_circuit_rating_forecast.additional_properties = d
        return predicted_circuit_rating_forecast

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

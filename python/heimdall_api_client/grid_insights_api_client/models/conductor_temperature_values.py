from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
import datetime






T = TypeVar("T", bound="ConductorTemperatureValues")



@_attrs_define
class ConductorTemperatureValues:
    """ 
        Attributes:
            timestamp (datetime.datetime): Time (in UTC) when the conductor temperature was measured. Example:
                2024-07-01T12:00:00Z.
            max_ (float): The maximum conductor temperature measured for the line at the given timestamp. Example: 68.7.
            min_ (Union[None, Unset, float]): The minimum conductor temperature measured for the line at the given
                timestamp. Example: 55.2.
     """

    timestamp: datetime.datetime
    max_: float
    min_: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        max_ = self.max_

        min_: Union[None, Unset, float]
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timestamp": timestamp,
            "max": max_,
        })
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))




        max_ = d.pop("max")

        def _parse_min_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        min_ = _parse_min_(d.pop("min", UNSET))


        conductor_temperature_values = cls(
            timestamp=timestamp,
            max_=max_,
            min_=min_,
        )


        conductor_temperature_values.additional_properties = d
        return conductor_temperature_values

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

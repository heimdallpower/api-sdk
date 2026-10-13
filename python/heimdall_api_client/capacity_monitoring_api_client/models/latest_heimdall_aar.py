from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.heimdall_aar import HeimdallAar
    from ..models.latest_heimdall_span_aar import LatestHeimdallSpanAar


T = TypeVar("T", bound="LatestHeimdallAar")


@_attrs_define
class LatestHeimdallAar:
    """
    Attributes:
        metric (str): A human-readable label identifying the rating returned by this endpoint, independent of the
            `quantity` query parameter. Example: Heimdall AAR.
        unit (str): The unit of the value in the response. Depends on the requested `quantity` query parameter:
              - `current` (default) → `"Ampere"`
              - `apparent_power` → `"MVA"`
             Example: Ampere.
        heimdall_aar (HeimdallAar):
        heimdall_span_aars (list[LatestHeimdallSpanAar] | None | Unset): Per-span breakdown of the latest Heimdall AAR,
            calculated at the same timestamp as `heimdall_aar`. Spans without a Heimdall AAR at that timestamp are omitted.
            Only present when `include=spans` is set on the request; otherwise `null`.
    """

    metric: str
    unit: str
    heimdall_aar: HeimdallAar
    heimdall_span_aars: list[LatestHeimdallSpanAar] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        heimdall_aar = self.heimdall_aar.to_dict()

        heimdall_span_aars: list[dict[str, Any]] | None | Unset
        if isinstance(self.heimdall_span_aars, Unset):
            heimdall_span_aars = UNSET
        elif isinstance(self.heimdall_span_aars, list):
            heimdall_span_aars = []
            for heimdall_span_aars_type_0_item_data in self.heimdall_span_aars:
                heimdall_span_aars_type_0_item = heimdall_span_aars_type_0_item_data.to_dict()
                heimdall_span_aars.append(heimdall_span_aars_type_0_item)

        else:
            heimdall_span_aars = self.heimdall_span_aars

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "heimdall_aar": heimdall_aar,
            }
        )
        if heimdall_span_aars is not UNSET:
            field_dict["heimdall_span_aars"] = heimdall_span_aars

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.heimdall_aar import HeimdallAar
        from ..models.latest_heimdall_span_aar import LatestHeimdallSpanAar

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        heimdall_aar = HeimdallAar.from_dict(d.pop("heimdall_aar"))

        def _parse_heimdall_span_aars(data: object) -> list[LatestHeimdallSpanAar] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                heimdall_span_aars_type_0 = []
                _heimdall_span_aars_type_0 = data
                for heimdall_span_aars_type_0_item_data in _heimdall_span_aars_type_0:
                    heimdall_span_aars_type_0_item = LatestHeimdallSpanAar.from_dict(
                        heimdall_span_aars_type_0_item_data
                    )

                    heimdall_span_aars_type_0.append(heimdall_span_aars_type_0_item)

                return heimdall_span_aars_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[LatestHeimdallSpanAar] | None | Unset, data)

        heimdall_span_aars = _parse_heimdall_span_aars(d.pop("heimdall_span_aars", UNSET))

        latest_heimdall_aar = cls(
            metric=metric,
            unit=unit,
            heimdall_aar=heimdall_aar,
            heimdall_span_aars=heimdall_span_aars,
        )

        latest_heimdall_aar.additional_properties = d
        return latest_heimdall_aar

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

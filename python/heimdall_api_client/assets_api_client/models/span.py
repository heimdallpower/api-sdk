from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.span_phase import SpanPhase





T = TypeVar("T", bound="Span")



@_attrs_define
class Span:
    """ 
        Attributes:
            id (UUID): Unique identifier of the span. Example: 00000000-0000-0000-0000-000000000000.
            span_phases (list['SpanPhase']): List of span phases associated with the span.
            mast_name_a (Union[None, Unset, str]):
            mast_name_b (Union[None, Unset, str]):
     """

    id: UUID
    span_phases: list['SpanPhase']
    mast_name_a: Union[None, Unset, str] = UNSET
    mast_name_b: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        span_phases = []
        for span_phases_item_data in self.span_phases:
            span_phases_item = span_phases_item_data.to_dict()
            span_phases.append(span_phases_item)



        mast_name_a: Union[None, Unset, str]
        if isinstance(self.mast_name_a, Unset):
            mast_name_a = UNSET
        else:
            mast_name_a = self.mast_name_a

        mast_name_b: Union[None, Unset, str]
        if isinstance(self.mast_name_b, Unset):
            mast_name_b = UNSET
        else:
            mast_name_b = self.mast_name_b


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "span_phases": span_phases,
        })
        if mast_name_a is not UNSET:
            field_dict["mast_name_a"] = mast_name_a
        if mast_name_b is not UNSET:
            field_dict["mast_name_b"] = mast_name_b

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_phase import SpanPhase
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        span_phases = []
        _span_phases = d.pop("span_phases")
        for span_phases_item_data in (_span_phases):
            span_phases_item = SpanPhase.from_dict(span_phases_item_data)



            span_phases.append(span_phases_item)


        def _parse_mast_name_a(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mast_name_a = _parse_mast_name_a(d.pop("mast_name_a", UNSET))


        def _parse_mast_name_b(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mast_name_b = _parse_mast_name_b(d.pop("mast_name_b", UNSET))


        span = cls(
            id=id,
            span_phases=span_phases,
            mast_name_a=mast_name_a,
            mast_name_b=mast_name_b,
        )


        span.additional_properties = d
        return span

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

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union






T = TypeVar("T", bound="ProblemDetails")



@_attrs_define
class ProblemDetails:
    """ 
        Attributes:
            type_ (Union[Unset, str]):
            title (Union[Unset, str]):
            status (Union[Unset, int]):
            detail (Union[Unset, str]):
            instance (Union[Unset, str]):
     """

    type_: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    detail: Union[Unset, str] = UNSET
    instance: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        detail = self.detail

        instance = self.instance


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if title is not UNSET:
            field_dict["title"] = title
        if status is not UNSET:
            field_dict["status"] = status
        if detail is not UNSET:
            field_dict["detail"] = detail
        if instance is not UNSET:
            field_dict["instance"] = instance

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        title = d.pop("title", UNSET)

        status = d.pop("status", UNSET)

        detail = d.pop("detail", UNSET)

        instance = d.pop("instance", UNSET)

        problem_details = cls(
            type_=type_,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
        )


        problem_details.additional_properties = d
        return problem_details

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

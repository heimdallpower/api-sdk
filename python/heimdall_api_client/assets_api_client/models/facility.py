from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from uuid import UUID

if TYPE_CHECKING:
  from ..models.line import Line





T = TypeVar("T", bound="Facility")



@_attrs_define
class Facility:
    """ 
        Attributes:
            id (UUID): Unique identifier of the facility. Example: 00000000-0000-0000-0000-000000000000.
            name (str): Name of the facility. Example: Facility A.
            line (Line):
     """

    id: UUID
    name: str
    line: 'Line'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        line = self.line.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "line": line,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line import Line
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        line = Line.from_dict(d.pop("line"))




        facility = cls(
            id=id,
            name=name,
            line=line,
        )


        facility.additional_properties = d
        return facility

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

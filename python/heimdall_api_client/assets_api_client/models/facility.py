from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union
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
            line (Union['Line', None, Unset]): Line associated with the facility, if available.
     """

    id: UUID
    name: str
    line: Union['Line', None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.line import Line
        id = str(self.id)

        name = self.name

        line: Union[None, Unset, dict[str, Any]]
        if isinstance(self.line, Unset):
            line = UNSET
        elif isinstance(self.line, Line):
            line = self.line.to_dict()
        else:
            line = self.line


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
        })
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line import Line
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        def _parse_line(data: object) -> Union['Line', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                line_type_0 = Line.from_dict(data)



                return line_type_0
            except: # noqa: E722
                pass
            return cast(Union['Line', None, Unset], data)

        line = _parse_line(d.pop("line", UNSET))


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

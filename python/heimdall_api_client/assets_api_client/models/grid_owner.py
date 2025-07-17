from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.facility import Facility





T = TypeVar("T", bound="GridOwner")



@_attrs_define
class GridOwner:
    """ 
        Attributes:
            name (str): Name of the grid owner. Example: Grid owner A.
            facilities (list['Facility']): List of facilities associated with the grid owner.
     """

    name: str
    facilities: list['Facility']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        facilities = []
        for facilities_item_data in self.facilities:
            facilities_item = facilities_item_data.to_dict()
            facilities.append(facilities_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "facilities": facilities,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facility import Facility
        d = dict(src_dict)
        name = d.pop("name")

        facilities = []
        _facilities = d.pop("facilities")
        for facilities_item_data in (_facilities):
            facilities_item = Facility.from_dict(facilities_item_data)



            facilities.append(facilities_item)


        grid_owner = cls(
            name=name,
            facilities=facilities,
        )


        grid_owner.additional_properties = d
        return grid_owner

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

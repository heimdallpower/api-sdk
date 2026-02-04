from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.grid_owner import GridOwner





T = TypeVar("T", bound="Assets")



@_attrs_define
class Assets:
    """ 
        Attributes:
            grid_owners (list['GridOwner']): List of grid owners the API consumer has access to.
     """

    grid_owners: list['GridOwner']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grid_owner import GridOwner
        grid_owners = []
        for grid_owners_item_data in self.grid_owners:
            grid_owners_item = grid_owners_item_data.to_dict()
            grid_owners.append(grid_owners_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "grid_owners": grid_owners,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grid_owner import GridOwner
        d = dict(src_dict)
        grid_owners = []
        _grid_owners = d.pop("grid_owners")
        for grid_owners_item_data in (_grid_owners):
            grid_owners_item = GridOwner.from_dict(grid_owners_item_data)



            grid_owners.append(grid_owners_item)


        assets = cls(
            grid_owners=grid_owners,
        )


        assets.additional_properties = d
        return assets

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

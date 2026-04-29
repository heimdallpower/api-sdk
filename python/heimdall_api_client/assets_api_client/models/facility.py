from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facility_component import FacilityComponent
    from ..models.line_type_0 import LineType0


T = TypeVar("T", bound="Facility")


@_attrs_define
class Facility:
    """
    Attributes:
        id (UUID): Unique identifier of the facility. Example: 00000000-0000-0000-0000-000000000000.
        name (str): Name of the facility. Example: Facility A.
        components (list[FacilityComponent]): List of facility components belonging to the facility.
        line (LineType0 | None | Unset):
    """

    id: UUID
    name: str
    components: list[FacilityComponent]
    line: LineType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.line_type_0 import LineType0

        id = str(self.id)

        name = self.name

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        line: dict[str, Any] | None | Unset
        if isinstance(self.line, Unset):
            line = UNSET
        elif isinstance(self.line, LineType0):
            line = self.line.to_dict()
        else:
            line = self.line

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "components": components,
            }
        )
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facility_component import FacilityComponent
        from ..models.line_type_0 import LineType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = FacilityComponent.from_dict(components_item_data)

            components.append(components_item)

        def _parse_line(data: object) -> LineType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_line_type_0 = LineType0.from_dict(data)

                return componentsschemas_line_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LineType0 | None | Unset, data)

        line = _parse_line(d.pop("line", UNSET))

        facility = cls(
            id=id,
            name=name,
            components=components,
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

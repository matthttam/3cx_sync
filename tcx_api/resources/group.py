from pydantic import TypeAdapter
import requests
from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import TcxStrEnum
from tcx_api.components.schemas.pbx import Group
from tcx_api.components.parameters import (
    ExpandParameters,
    ListParameters,
    OrderbyParameters,
    SelectParameters,
)
from tcx_api import exceptions as TCX_Exceptions


class GroupProperties(TcxStrEnum):
    AllowCallService = auto()
    AnswerAfter = auto()
    BreakRoute = auto()
    BreakTime = auto()
    CallHandlingMode = auto()
    CallUsEnableChat = auto()
    CallUsEnablePhone = auto()
    CallUsEnableVideo = auto()
    CallUsRequirement = auto()
    ClickToCallId = auto()
    CurrentGroupHours = auto()
    CustomOperator = auto()
    CustomPrompt = auto()
    DisableCustomPrompt = auto()
    GloballyVisible = auto()
    Groups = auto()
    HasMembers = auto()
    HolidaysRoute = auto()
    Hours = auto()
    Id = auto()
    IsDefault = auto()
    Language = auto()
    LastLoginTime = auto()
    Members = auto()
    Name = auto()
    Number = auto()
    OfficeHolidays = auto()
    OfficeRoute = auto()
    OutOfOfficeRoute = auto()
    OverrideExpiresAt = auto()
    OverrideHolidays = auto()
    PromptSet = auto()
    Props = auto()
    Rights = auto()
    TimeZoneId = auto()


class ListGroupParameters(
    ListParameters,
    OrderbyParameters,
    SelectParameters[GroupProperties],
    ExpandParameters,
): ...


class GetGroupParameters(SelectParameters[GroupProperties], ExpandParameters): ...


class GroupResource(APIResource):
    endpoint: str = "Groups"

    def list_group(self, params: ListGroupParameters) -> List[Group]:
        """Get entities from Groups"""
        try:
            response = self.api.get(self.endpoint, params)
            response_value = response.json().get("value")
            return TypeAdapter(List[Group]).validate_python(response_value)
        except requests.HTTPError as e:
            raise TCX_Exceptions.GroupListError(e)

    def create_group(self, group: Group):
        """Add new entity to Groups"""
        default_group_dict = self.get_group_defaults
        group_dict = group.model_dump(exclude_none=True, exclude_unset=True)
        merged_group_dict = default_group_dict | group_dict
        try:
            self.api.post(self.endpoint, merged_group_dict)
        except requests.HTTPError as e:
            raise TCX_Exceptions.GroupCreateError(e)

    def get_group(self, id: int, params: GetGroupParameters) -> Group:
        try:
            response = self.api.get(endpoint=f"Groups({id})", params=params)
            return TypeAdapter(Group).validate_python(response.json())
        except requests.HTTPError as e:
            raise TCX_Exceptions.GroupGetError(e)

    def update_group(self, group: Group):
        """Update a group entity"""
        try:
            group_dict = group.model_dump(
                exclude_unset=True,
                exclude_none=True,
                serialize_as_any=True,
                by_alias=True,
            )
            self.api.patch(endpoint=f"{self.endpoint}({group.Id})", data=group_dict)
        except requests.HTTPError as e:
            raise TCX_Exceptions.GroupUpdateError(e)

    def delete_group(self, group: Group):
        if isinstance(group, Group):
            self.api.delete(endpoint=self.endpoint, params=group.Id)

    def get_group_defaults(self):
        return {}

    def get_default_group(self):
        groups = self.list_group(params=ListGroupParameters(filter="IsDefault eq true"))
        return groups.pop()

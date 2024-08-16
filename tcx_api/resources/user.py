import json
import requests

from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import TcxStrEnum

from pydantic import TypeAdapter
from tcx_api.components.schemas.ODataErrors import MainError
from tcx_api.components.schemas.pbx import User
from tcx_api.components.parameters import GetParameters, ListParameters
from tcx_api import exceptions as TCX_Exceptions


class UserProperties(TcxStrEnum):
    AccessPassword = auto()
    AllowLanOnly = auto()
    AllowOwnRecordings = auto()
    AuthID = auto()
    AuthPassword = auto()
    Blfs = auto()
    BreakTime = auto()
    CallScreening = auto()
    CallUsEnableChat = auto()
    CallUsEnablePhone = auto()
    CallUsEnableVideo = auto()
    CallUsRequirement = auto()
    ClickToCallId = auto()
    ContactImage = auto()
    CurrentProfileName = auto()
    DeskphonePassword = auto()
    DisplayName = auto()
    EmailAddress = auto()
    Enable2FA = auto()
    Enabled = auto()
    EnableHotdesking = auto()
    FirstName = auto()
    ForwardingExceptions = auto()
    ForwardingProfiles = auto()
    GoogleSignInEnabled = auto()
    Greetings = auto()
    Groups = auto()
    HideInPhonebook = auto()
    HotdeskingAssignment = auto()
    Hours = auto()
    Id = auto()
    Internal = auto()
    IsRegistered = auto()
    Language = auto()
    LastName = auto()
    Mobile = auto()
    MS365CalendarEnabled = auto()
    MS365ContactsEnabled = auto()
    MS365SignInEnabled = auto()
    MS365TeamsEnabled = auto()
    MyPhoneAllowDeleteRecordings = auto()
    MyPhoneHideForwardings = auto()
    MyPhonePush = auto()
    MyPhoneShowRecordings = auto()
    Number = auto()
    OfficeHoursProps = auto()
    OutboundCallerID = auto()
    Phones = auto()
    PinProtected = auto()
    PinProtectTimeout = auto()
    PrimaryGroupId = auto()
    PromptSet = auto()
    ProvFile = auto()
    ProvLink = auto()
    RecordCalls = auto()
    RecordExternalCallsOnly = auto()
    Require2FA = auto()
    SendEmailMissedCalls = auto()
    SIPID = auto()
    Tags = auto()
    VMDisablePinAuth = auto()
    VMEmailOptions = auto()
    VMEnabled = auto()
    VMPIN = auto()
    VMPlayCallerID = auto()
    VMPlayMsgDateTime = auto()
    WebMeetingApproveParticipants = auto()
    WebMeetingFriendlyName = auto()


class ListUserParameters(ListParameters):
    """
    Parameters for listing users.

    Attributes:
        top (int): The number of items to retrieve from the top.
        skip (int): The number of items to skip.
        search (str): The search query.
        filter (str): The filter to apply.
        count (bool): Indicates if a count should be returned or not.
        orderby (str): The field to order by.
        select (list): Select properties to be returned.
        expand (str): Expand related entities.

    """

    orderby: str = None
    select: List[UserProperties] = None
    expand: str = None


class GetUserParameters(GetParameters):
    select: List[UserProperties] = None


class UserResource(APIResource):
    endpoint: str = "Users"

    def list_user(self, params: ListUserParameters) -> List[User]:
        """Get entities from Users"""
        try:
            response = self.api.get(self.endpoint, params)
            response_value = response.json().get("value")
            return TypeAdapter(List[User]).validate_python(response_value)
        except requests.HTTPError as e:
            raise TCX_Exceptions.UserListError(e)

    def create_user(self, user: User):
        """Add new entity to Users"""
        default_user_dict = self.default_user
        user_dict = user.model_dump(
            exclude_none=True, exclude_unset=True)
        merged_user_dict = default_user_dict | user_dict
        try:
            self.api.post(self.endpoint, merged_user_dict)
        except requests.HTTPError as e:
            raise TCX_Exceptions.UserCreateError(e)

    def get_user(self, id: int, params: GetUserParameters) -> User:
        try:
            response = self.api.get(endpoint=f"Users({id})", params=params)
            return TypeAdapter(User).validate_python(response.json())
        except requests.HTTPError as e:
            raise TCX_Exceptions.UserGetError(e)

    def update_user(self, user: User):
        """Update a user entity"""
        user_dict = user.model_dump(exclude_unset=True,
                                    exclude_none=True, serialize_as_any=True)
        try:
            self.api.patch(
                endpoint=f"{self.endpoint}({user.Id})", data=user_dict)
        except requests.HTTPError as e:
            raise TCX_Exceptions.UserUpdateError(e)

    def delete_user(self, user: User | int):
        if isinstance(user, User):
            return self._delete_user_directly(user=user)
        return self._delete_user_by_id(id=user.Id)

    def _delete_user_directly(self, user: User):
        self._delete_user_by_id(id=user.Id)

    def _delete_user_by_id(self, id: int):
        """Delete entity from Users"""
        self.api.delete(endpoint=self.endpoint, params=id)
        # Looks like it takes a header value called If-Match that is a string of an etag.
        # Not sure if it is required.
        # - name: If-Match
        #  in: header
        #  description: ETag
        #  schema:
        #    type: string)

    @property
    def default_user(self):
        return json.loads('{"Require2FA": true, "SendEmailMissedCalls": true, "AuthID": "2cCY2wrcBU", "Phones": [], "Groups": [{"GroupId": 3078, "Rights": {"RoleName": "users"}}], "CallUsEnableChat": true, "CallUsRequirement": "Both", "ClickToCallId": "testtest", "EmailAddress": "", "Mobile": "", "FirstName": "TEST", "LastName": "TEST", "Number": "10003", "OutboundCallerID": "", "PrimaryGroupId": 3078, "WebMeetingFriendlyName": "testtest", "WebMeetingApproveParticipants": false, "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>", "ForwardingProfiles": [], "MS365CalendarEnabled": true, "MS365ContactsEnabled": true, "MS365SignInEnabled": true, "MS365TeamsEnabled": true, "GoogleSignInEnabled": true, "Enabled": true, "Internal": false, "AllowOwnRecordings": false, "MyPhoneShowRecordings": false, "MyPhoneAllowDeleteRecordings": false, "MyPhoneHideForwardings": false, "RecordCalls": false, "HideInPhonebook": false, "PinProtected": false, "CallScreening": false, "AllowLanOnly": true, "SIPID": "", "EnableHotdesking": false, "PbxDeliversAudio": false, "SRTPMode": "SRTPDisabled", "Hours": {"Type": "OfficeHours"}, "OfficeHoursProps": [], "BreakTime": {"Type": "OfficeHours"}, "VMEnabled": true, "VMPIN": "923080", "VMEmailOptions": "Notification", "VMDisablePinAuth": false, "VMPlayCallerID": false, "VMPlayMsgDateTime": "None", "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB", "Greetings": [{"Type": "Default", "Filename": ""}]}')

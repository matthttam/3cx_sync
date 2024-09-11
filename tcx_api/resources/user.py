import string
import random
from pydantic import TypeAdapter
import requests

from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import TcxStrEnum


from tcx_api.components.schemas.pbx import User
from tcx_api.components.parameters import (
    ExpandParameters,
    ListParameters,
    OrderbyParameters,
    SelectParameters,
)
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


class ListUserParameters(
    ListParameters,
    OrderbyParameters,
    SelectParameters[UserProperties],
    ExpandParameters,
): ...


class GetUserParameters(SelectParameters[UserProperties], ExpandParameters): ...


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

    def create_user(self, user: dict):
        """Add new entity to Users"""
        # new_user_dict = self.get_new_user
        # user_dict = user.model_dump(
        #    exclude_none=True, exclude_unset=True)
        # merged_user_dict = new_user_dict | user_dict

        try:
            self.api.post(self.endpoint, user)
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
        try:
            user_dict = user.model_dump(
                exclude_unset=True,
                exclude_none=True,
                serialize_as_any=True,
                by_alias=True,
            )
            self.api.patch(endpoint=f"{self.endpoint}({user.Id})", data=user_dict)
        except requests.HTTPError as e:
            raise TCX_Exceptions.UserUpdateError(e)

    def delete_user(self, user: User):
        if isinstance(user, User):
            self.api.delete(endpoint=self.endpoint, params=user.Id)

    def get_new_user(self):
        auth_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        # return json.loads('{"Require2FA": true, "SendEmailMissedCalls": true, "AuthID": "", "Phones": [], "Groups": [{"GroupId": 3078, "Rights": {"RoleName": "users"}}], "CallUsEnableChat": true, "CallUsRequirement": "Both", "ClickToCallId": "testtest", "EmailAddress": "", "Mobile": "", "FirstName": "TEST", "LastName": "TEST", "Number": "10003", "OutboundCallerID": "", "PrimaryGroupId": 3078, "WebMeetingFriendlyName": "testtest", "WebMeetingApproveParticipants": false, "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>", "ForwardingProfiles": [], "MS365CalendarEnabled": true, "MS365ContactsEnabled": true, "MS365SignInEnabled": true, "MS365TeamsEnabled": true, "GoogleSignInEnabled": true, "Enabled": true, "Internal": false, "AllowOwnRecordings": false, "MyPhoneShowRecordings": false, "MyPhoneAllowDeleteRecordings": false, "MyPhoneHideForwardings": false, "RecordCalls": false, "HideInPhonebook": false, "PinProtected": false, "CallScreening": false, "AllowLanOnly": true, "SIPID": "", "EnableHotdesking": false, "PbxDeliversAudio": false, "SRTPMode": "SRTPDisabled", "Hours": {"Type": "OfficeHours"}, "OfficeHoursProps": [], "BreakTime": {"Type": "OfficeHours"}, "VMEnabled": true, "VMPIN": "923080", "VMEmailOptions": "Notification", "VMDisablePinAuth": false, "VMPlayCallerID": false, "VMPlayMsgDateTime": "None", "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB", "Greetings": [{"Type": "Default", "Filename": ""}]}')
        return {
            "Require2FA": True,
            "SendEmailMissedCalls": True,
            "AuthID": auth_id,
            "Phones": [],
            "Groups": [],
            "CallUsEnableChat": True,
            "CallUsRequirement": "Both",
            "ClickToCallId": "",
            "EmailAddress": "",
            "Mobile": "",
            "FirstName": "",
            "LastName": "",
            "Number": "",
            "OutboundCallerID": "",
            "PrimaryGroupId": 3078,
            "WebMeetingFriendlyName": "",
            "WebMeetingApproveParticipants": False,
            "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>",
            "ForwardingProfiles": [],
            "MS365CalendarEnabled": True,
            "MS365ContactsEnabled": True,
            "MS365SignInEnabled": True,
            "MS365TeamsEnabled": True,
            "GoogleSignInEnabled": True,
            "Enabled": True,
            "Internal": False,
            "AllowOwnRecordings": False,
            "MyPhoneShowRecordings": False,
            "MyPhoneAllowDeleteRecordings": False,
            "MyPhoneHideForwardings": False,
            "RecordCalls": False,
            "HideInPhonebook": False,
            "PinProtected": False,
            "CallScreening": False,
            "AllowLanOnly": True,
            "SIPID": "",
            "EnableHotdesking": False,
            "PbxDeliversAudio": False,
            "SRTPMode": "SRTPDisabled",
            "Hours": {"Type": "OfficeHours"},
            "OfficeHoursProps": [],
            "BreakTime": {"Type": "OfficeHours"},
            "VMEnabled": True,
            "VMPIN": "",
            "VMEmailOptions": "Notification",
            "VMDisablePinAuth": False,
            "VMPlayCallerID": False,
            "VMPlayMsgDateTime": "None",
            "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB",
            "Greetings": [{"Type": "Default", "Filename": ""}],
        }

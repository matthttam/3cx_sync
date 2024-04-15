from tcx_api.components.parameters import GetParameters, ListParameters
from .api_resource import APIResource
from tcx_api.components.schemas.pbx.user import User
from enum import auto
from tcx_api.util import TcxStrEnum
from sync.factories.user_entity_factory import UserEntityFactory
from typing import List
from pydantic import TypeAdapter


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
        except Exception as e:
            print(f"Unknown Error. Failed to fetch users: {e}")
            return None

    def create_user(self, user: User):
        """Add new entity to Users"""
        self.api.post(self.endpoint, user.model_dump())

    def get_user(self, params: GetUserParameters, id: int) -> User:
        try:
            response = self.api.get(f"Users({id})", params=params)
            return TypeAdapter(User).validate_python(response.json())
        except Exception as e:
            # Handle exceptions appropriately
            print(f"Unknown Error. Failed to fetch user with id {id}: {e}")
            return None

    def update_user(self, user: User):
        """Update entity in Users"""
        try:
            response = self.api.patch(endpoint=self.endpoint, params=user.Id, data=user)
            return response.json()["value"]
        except Exception as e:
            print(f"Failed to update user: {e}")
            return None

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

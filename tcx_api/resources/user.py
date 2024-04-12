from tcx_api.api import API
from tcx_api.components.parameters import Parameters
from .api_resource import APIResource
from tcx_api.components.schemas.pbx.user import User
from enum import auto
from tcx_api.util import TcxStrEnum
from sync.factories.user_entity_factory import UserEntityFactory
from dataclasses import dataclass, asdict, field
from tcx_api.tcx_api_connection import TCX_API_Connection


@dataclass
class ListUserParameters(Parameters):
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

    top: int = None
    skip: int = None
    search: str = None
    filter: str = None
    count: bool = None
    orderby: str = None
    select: list[str] = None
    expand: str = None

    def __post_init__(self):
        if self.select is not None:
            self.validate_field(self.select)

        if self.top:
            self.validate_top(self.top)

        if self.skip:
            self.validate_skip(self.skip)

    def to_dict(self):
        """
        Convert Parameters instance to a dictionary, excluding attributes with value None.
        """
        return {k.lstrip("_"): v for k, v in asdict(self).items() if v is not None}

    def validate_field(self, value: list | str):
        if value is None:
            return

        if isinstance(value, list):
            invalid_fields = [field for field in value if field not in UserProperties]
        else:
            invalid_fields = value if value not in UserProperties else None
        if invalid_fields:
            raise ValueError(
                f"The following fields are not valid attributes of the User class: {invalid_fields}"
            )

    def validate_top(self, top: int):
        if top < 0:
            raise ValueError("top must be greater than or equal to 0")

    def validate_skip(self, skip: int):
        if skip < 0:
            raise ValueError("skip must be greater than or equal to 0")


class UserResource(APIResource):
    endpoint = "Users"

    def __init__(self, api: TCX_API_Connection):
        super().__init__(api=api)

    def list_user(self, params: ListUserParameters):
        """Get entities from Users"""
        try:
            response = self.api.get("Users", params)
            users = response.json().get("value", None)
            if users:
                return [UserEntityFactory.create_user(**user) for user in users]
            else:
                return None
        except Exception as e:
            print(f"Failed to fetch users: {e}")
            return None

    def create_user(self, user: User):
        """Add new entity to Users"""
        pass

    def get_user(self, id):
        try:
            response = self.api.get("Users")
            users = response.json()["value"]
            return users
        except Exception as e:
            # Handle exceptions appropriately
            print(f"Failed to fetch users: {e}")
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
            self.delete_user_directly(user=user)
        else:
            self.delete_user_by_id(id=user.Id)

    def delete_user_directly(self, user: User):
        self.delete_user_by_id(id=user.Id)

    def delete_user_by_id(self, id: int):
        """Delete entity from Users"""
        self.api.delete(endpoint=self.endpoint, params=id)
        # Looks like it takes a header value called If-Match that is a string of an etag.
        # Not sure if it is required.
        # - name: If-Match
        #  in: header
        #  description: ETag
        #  schema:
        #    type: string


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

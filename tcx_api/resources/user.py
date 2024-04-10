from tcx_api.api import API
from .api_resource import APIResource
from enum import auto, StrEnum
from typing import List, Optional, Dict
from typing import TypedDict, Unpack


class UserProperties(StrEnum):
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


# class UserEntity:
#    def __init__(self, **kwargs):
#        self.properties = {}
#        for key, value in kwargs.items():
#            if key not in UserProperties.__members__:
#                raise ValueError(f"Invalid property: {key}")
#
#            match key:
#                case "BreakTime":
#                    value = Pbx_Schedule(**value)
#                case "CallUsRequirement":
#                    value = Pbx_Authentication(value)
#
#            setattr(self, key, value)


class ListUserParameters(TypedDict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    top: int = None
    skip: int = None
    search: str = None
    filter: str = None
    count: bool = None
    orderby: str = None
    select: Optional[List[UserProperties]] = None
    expand: str = None


class UserResource(APIResource):

    def __init__(self, api: API):
        super().__init__(api=api)

    # Methods
    def list_user(self, **kwargs: Unpack[ListUserParameters]) -> List[Dict]:
        """Get entities from Users"""
        try:

            # Validate select
            if kwargs.get("select"):
                self.validate_user_properties(kwargs["select"])

            response = self.api.get("Users", ListUserParameters(kwargs))
            return response.json()["value"]
        except Exception as e:
            print(f"Failed to fetch users: {e}")
            return None

    def create_user(self, user):
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

    def update_user(self, user):
        pass

    def delete_user(self, id):
        pass

    # Validate User Properties
    def validate_user_properties(self, properties: List[str]):
        if not set(UserProperties).issuperset(properties):
            raise ValueError(f"Only {[v.value for v in UserProperties]} are allowed.")

from tcx_api.api import API
from .api_resource import APIResource
from enum import auto, StrEnum
from typing import List, Optional, Dict
from typing import TypedDict, Unpack
from tcx_api.components.schemas import (
    Pbx_Greeting,
    Pbx_OfficeHoursBits,
    Pbx_Schedule,
    Pbx_Authentication,
    Pbx_ExtensionRule,
    Pbx_ForwardingProfile,
    Pbx_Phone,
    Pbx_UserGroup,
    Pbx_UserTag,
    Pbx_VMEmailOptionsType,
    Pbx_VMPlayMsgDateTimeType,
)


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


class UserEntity:
    def __init__(
        self,
        AccessPassword: str = None,
        AllowLanOnly: bool = None,
        AllowOwnRecordings: bool = None,
        AuthID: str = None,
        AuthPassword: str = None,
        Blfs: str = None,
        BreakTime: Pbx_Schedule = None,
        CallScreening: bool = None,
        CallUsEnableChat: bool = None,
        CallUsEnablePhone: bool = None,
        CallUsEnableVideo: bool = None,
        CallUsRequirement: Pbx_Authentication = None,
        ClickToCallId: str = None,
        ContactImage: str = None,
        CurrentProfileName: str = None,
        DeskphonePassword: str = None,
        DisplayName: str = None,
        EmailAddress: str = None,
        Enable2FA: bool = None,
        Enabled: bool = None,
        EnableHotdesking: bool = None,
        FirstName: str = None,
        ForwardingExceptions: List[Pbx_ExtensionRule] = None,
        ForwardingProfiles: List[Pbx_ForwardingProfile] = None,
        GoogleSignInEnabled: bool = None,
        Greetings: List[Pbx_Greeting] = None,
        Groups: List[Pbx_UserGroup] = None,
        HideInPhonebook: bool = None,
        HotdeskingAssignment: str = None,
        Hours: List[Pbx_Schedule] = None,
        Id: int = None,
        Internal: bool = None,
        IsRegistered: bool = None,
        Language: str = None,
        LastName: str = None,
        Mobile: str = None,
        MS365CalendarEnabled: bool = None,
        MS365ContactsEnabled: bool = None,
        MS365SignInEnabled: bool = None,
        MS365TeamsEnabled: bool = None,
        MyPhoneAllowDeleteRecordings: bool = None,
        MyPhoneHideForwardings: bool = None,
        MyPhonePush: bool = None,
        MyPhoneShowRecordings: bool = None,
        Number: str = None,
        OfficeHoursProps: List[Pbx_OfficeHoursBits] = None,
        OutboundCallerID: str = None,
        Phones: List[Pbx_Phone] = None,
        PinProtected: bool = None,
        PinProtectTimeout: int = None,
        PrimaryGroupId: int = None,
        PromptSet: str = None,
        ProvFile: str = None,
        ProvLink: str = None,
        RecordCalls: bool = None,
        RecordExternalCallsOnly: bool = None,
        Require2FA: bool = None,
        SendEmailMissedCalls: bool = None,
        SIPID: str = None,
        Tags: List[Pbx_UserTag] = None,
        VMDisablePinAuth: bool = None,
        VMEmailOptions: Pbx_VMEmailOptionsType = None,
        VMEnabled: bool = None,
        VMPIN: str = None,
        VMPlayCallerID: bool = None,
        VMPlayMsgDateTime: Pbx_VMPlayMsgDateTimeType = None,
        WebMeetingApproveParticipants: bool = None,
        WebMeetingFriendlyName: str = None,
    ):
        self.AccessPassword = AccessPassword
        self.AllowLanOnly = AllowLanOnly
        self.AllowOwnRecordings = AllowOwnRecordings
        self.AuthID = AuthID
        self.AuthPassword = AuthPassword
        self.Blfs = Blfs
        self.BreakTime = Pbx_Schedule(**BreakTime)
        self.CallScreening = CallScreening
        self.CallUsEnableChat = CallUsEnableChat
        self.CallUsEnablePhone = CallUsEnablePhone
        self.CallUsEnableVideo = CallUsEnableVideo
        self.CallUsRequirement = CallUsRequirement
        self.ClickToCallId = ClickToCallId
        self.ContactImage = ContactImage
        self.CurrentProfileName = CurrentProfileName
        self.DeskphonePassword = DeskphonePassword
        self.DisplayName = DisplayName
        self.EmailAddress = EmailAddress
        self.Enable2FA = Enable2FA
        self.Enabled = Enabled
        self.EnableHotdesking = EnableHotdesking
        self.FirstName = FirstName
        self.ForwardingExceptions = ForwardingExceptions
        self.ForwardingProfiles = ForwardingProfiles
        self.GoogleSignInEnabled = GoogleSignInEnabled
        self.Greetings = Greetings
        self.Groups = Groups
        self.HideInPhonebook = HideInPhonebook
        self.HotdeskingAssignment = HotdeskingAssignment
        self.Hours = Hours
        self.Id = Id
        self.Internal = Internal
        self.IsRegistered = IsRegistered
        self.Language = Language
        self.LastName = LastName
        self.Mobile = Mobile
        self.MS365CalendarEnabled = MS365CalendarEnabled
        self.MS365ContactsEnabled = MS365ContactsEnabled
        self.MS365SignInEnabled = MS365SignInEnabled
        self.MS365TeamsEnabled = MS365TeamsEnabled
        self.MyPhoneAllowDeleteRecordings = MyPhoneAllowDeleteRecordings
        self.MyPhoneHideForwardings = MyPhoneHideForwardings
        self.MyPhonePush = MyPhonePush
        self.MyPhoneShowRecordings = MyPhoneShowRecordings
        self.Number = Number
        Pbx_Authentication["None"]
        self.OfficeHoursProps = (
            [Pbx_OfficeHoursBits[e] for e in OfficeHoursProps]
            if OfficeHoursProps
            else None
        )

        self.OutboundCallerID = OutboundCallerID
        self.Phones = Phones
        self.PinProtected = PinProtected
        self.PinProtectTimeout = PinProtectTimeout
        self.PrimaryGroupId = PrimaryGroupId
        self.PromptSet = PromptSet
        self.ProvFile = ProvFile
        self.ProvLink = ProvLink
        self.RecordCalls = RecordCalls
        self.RecordExternalCallsOnly = RecordExternalCallsOnly
        self.Require2FA = Require2FA
        self.SendEmailMissedCalls = SendEmailMissedCalls
        self.SIPID = SIPID
        self.Tags = Tags
        self.VMDisablePinAuth = VMDisablePinAuth
        self.VMEmailOptions = VMEmailOptions
        self.VMEnabled = VMEnabled
        self.VMPIN = VMPIN
        self.VMPlayCallerID = VMPlayCallerID
        self.VMPlayMsgDateTime = VMPlayMsgDateTime
        self.WebMeetingApproveParticipants = WebMeetingApproveParticipants
        self.WebMeetingFriendlyName = WebMeetingFriendlyName


class UserFactory:
    @staticmethod
    def create_user(**kwargs):
        return UserEntity(**kwargs)


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

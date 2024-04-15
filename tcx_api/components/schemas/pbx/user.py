from tcx_api.components.schemas.pbx.user_group import UserGroup as UserGroupObject
from tcx_api.components.schemas.pbx.greeting import Greeting as GreetingObject
from tcx_api.components.schemas.pbx.phone import Phone as PhoneObject
from tcx_api.components.schemas.pbx.extension_rule import (
    ExtensionRule as ExtensionRuleObject,
)
from tcx_api.components.schemas.pbx.forwarding_profile import (
    ForwardingProfile as ForwardingProfileObject,
)
from tcx_api.components.schemas.pbx.schedule import Schedule as ScheduleObject

from tcx_api.components.schemas.pbx.enums import (
    Authentication as AuthenticationEnum,
    OfficeHoursBits as OfficeHoursBitsEnum,
    UserTag as UserTagEnum,
    VMEmailOptionsType as VMEmailOptionsTypeEnum,
    VMPlayMsgDateTimeType as VMPlayMsgDateTimeTypeEnum,
)

from tcx_api.components.schemas.schema import Schema
from pydantic import conlist


# @dataclass
class User(Schema):
    Id: int
    AccessPassword: str = None
    AllowLanOnly: bool = None
    AllowOwnRecordings: bool = None
    AuthID: str = None
    AuthPassword: str = None
    Blfs: str = None
    BreakTime: ScheduleObject = None
    CallScreening: bool = None
    CallUsEnableChat: bool = None
    CallUsEnablePhone: bool = None
    CallUsEnableVideo: bool = None
    CallUsRequirement: AuthenticationEnum = None
    ClickToCallId: str = None
    ContactImage: str = None
    CurrentProfileName: str = None
    DeskphonePassword: str = None
    DisplayName: str = None
    EmailAddress: str = None
    Enable2FA: bool = None
    Enabled: bool = None
    EnableHotdesking: bool = None
    FirstName: str = None
    ForwardingExceptions: conlist(ExtensionRuleObject) = None
    ForwardingProfiles: conlist(ForwardingProfileObject) = None
    GoogleSignInEnabled: bool = None
    Greetings: conlist(GreetingObject) = None
    Groups: conlist(UserGroupObject) = None
    HideInPhonebook: bool = None
    HotdeskingAssignment: str = None
    Hours: ScheduleObject = None
    Internal: bool = None
    IsRegistered: bool = None
    Language: str = None
    LastName: str = None
    Mobile: str = None
    MS365CalendarEnabled: bool = None
    MS365ContactsEnabled: bool = None
    MS365SignInEnabled: bool = None
    MS365TeamsEnabled: bool = None
    MyPhoneAllowDeleteRecordings: bool = None
    MyPhoneHideForwardings: bool = None
    MyPhonePush: bool = None
    MyPhoneShowRecordings: bool = None
    Number: str = None
    OfficeHoursProps: conlist(OfficeHoursBitsEnum) = None
    OutboundCallerID: str = None
    Phones: conlist(PhoneObject) = None
    PinProtected: bool = None
    PinProtectTimeout: int = None
    PrimaryGroupId: int = None
    PromptSet: str = None
    ProvFile: str = None
    ProvLink: str = None
    RecordCalls: bool = None
    RecordExternalCallsOnly: bool = None
    Require2FA: bool = None
    SendEmailMissedCalls: bool = None
    SIPID: str = None
    Tags: conlist(UserTagEnum) = None
    VMDisablePinAuth: bool = None
    VMEmailOptions: VMEmailOptionsTypeEnum = None
    VMEnabled: bool = None
    VMPIN: str = None
    VMPlayCallerID: bool = None
    VMPlayMsgDateTime: VMPlayMsgDateTimeTypeEnum = None
    WebMeetingApproveParticipants: bool = None
    WebMeetingFriendlyName: str = None

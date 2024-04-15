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
from typing import Optional


class User(Schema):
    Id: int
    AccessPassword: Optional[str] = None
    AllowLanOnly: Optional[bool] = None
    AllowOwnRecordings: Optional[bool] = None
    AuthID: Optional[str] = None
    AuthPassword: Optional[str] = None
    Blfs: Optional[str] = None
    BreakTime: Optional[ScheduleObject] = None
    CallScreening: Optional[bool] = None
    CallUsEnableChat: Optional[bool] = None
    CallUsEnablePhone: Optional[bool] = None
    CallUsEnableVideo: Optional[bool] = None
    CallUsRequirement: Optional[AuthenticationEnum] = None
    ClickToCallId: Optional[str] = None
    ContactImage: Optional[str] = None
    CurrentProfileName: Optional[str] = None
    DeskphonePassword: Optional[str] = None
    DisplayName: Optional[str] = None
    EmailAddress: Optional[str] = None
    Enable2FA: Optional[bool] = None
    Enabled: Optional[bool] = None
    EnableHotdesking: Optional[bool] = None
    FirstName: Optional[str] = None
    ForwardingExceptions: Optional[conlist(ExtensionRuleObject)] = None
    ForwardingProfiles: Optional[conlist(ForwardingProfileObject)] = None
    GoogleSignInEnabled: Optional[bool] = None
    Greetings: Optional[conlist(GreetingObject)] = None
    Groups: Optional[conlist(UserGroupObject)] = None
    HideInPhonebook: Optional[bool] = None
    HotdeskingAssignment: Optional[str] = None
    Hours: Optional[ScheduleObject] = None
    Internal: Optional[bool] = None
    IsRegistered: Optional[bool] = None
    Language: Optional[str] = None
    LastName: Optional[str] = None
    Mobile: Optional[str] = None
    MS365CalendarEnabled: Optional[bool] = None
    MS365ContactsEnabled: Optional[bool] = None
    MS365SignInEnabled: Optional[bool] = None
    MS365TeamsEnabled: Optional[bool] = None
    MyPhoneAllowDeleteRecordings: Optional[bool] = None
    MyPhoneHideForwardings: Optional[bool] = None
    MyPhonePush: Optional[bool] = None
    MyPhoneShowRecordings: Optional[bool] = None
    Number: Optional[str] = None
    OfficeHoursProps: Optional[conlist(OfficeHoursBitsEnum)] = None
    OutboundCallerID: Optional[str] = None
    Phones: Optional[conlist(PhoneObject)] = None
    PinProtected: Optional[bool] = None
    PinProtectTimeout: Optional[int] = None
    PrimaryGroupId: Optional[int] = None
    PromptSet: Optional[str] = None
    ProvFile: Optional[str] = None
    ProvLink: Optional[str] = None
    RecordCalls: Optional[bool] = None
    RecordExternalCallsOnly: Optional[bool] = None
    Require2FA: Optional[bool] = None
    SendEmailMissedCalls: Optional[bool] = None
    SIPID: Optional[str] = None
    Tags: Optional[conlist(UserTagEnum)] = None
    VMDisablePinAuth: Optional[bool] = None
    VMEmailOptions: Optional[VMEmailOptionsTypeEnum] = None
    VMEnabled: Optional[bool] = None
    VMPIN: Optional[str] = None
    VMPlayCallerID: Optional[bool] = None
    VMPlayMsgDateTime: Optional[VMPlayMsgDateTimeTypeEnum] = None
    WebMeetingApproveParticipants: Optional[bool] = None
    WebMeetingFriendlyName: Optional[str] = None

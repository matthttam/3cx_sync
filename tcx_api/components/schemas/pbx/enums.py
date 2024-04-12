from tcx_api.util import TcxStrEnum
from enum import auto


class Authentication(TcxStrEnum):
    Both = auto()
    Name = auto()
    Email = auto()
    NONE = auto()


class DayOfWeek(TcxStrEnum):
    Sunday = auto()
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()


class DestinationType(TcxStrEnum):
    NONE = auto()
    VoiceMail = auto()
    Extension = auto()
    Queue = auto()
    RingGroup = auto()
    IVR = auto()
    External = auto()
    Fax = auto()
    Boomerang = auto()
    Deflect = auto()
    VoiceMailOfDestination = auto()
    Callback = auto()
    RoutePoint = auto()
    ProceedWithNoExceptions = auto()


class OfficeHoursBits(TcxStrEnum):
    GlobalSchedule = auto()
    AutoSwitchProfiles = auto()
    AutoQueueLogOut = auto()
    BlockOutboundCalls = auto()


class PeerType(TcxStrEnum):
    Extension = auto()
    Queue = auto()
    RingGroup = auto()
    IVR = auto()
    Fax = auto()
    Conference = auto()
    Parking = auto()
    ExternalLine = auto()
    SpecialMenu = auto()
    Group = auto()
    RoutePoint = auto()


class RuleHoursType(TcxStrEnum):
    AllHours = auto()
    OfficeHours = auto()
    OutOfOfficeHours = auto()
    SpecificHours = auto()
    SpecificHoursExcludingHolidays = auto()
    OutOfSpecificHours = auto()
    OutOfSpecificHoursIncludingHolidays = auto()
    Never = auto()
    BreakTime = auto()


class ScheduleType(TcxStrEnum):
    Daily = auto()
    Weekly = auto()
    Monthly = auto()
    Hourly = auto()
    Immediate = auto()


class UserTag(TcxStrEnum):
    MS = auto()
    Teams = auto()
    Google = auto()
    WakeUp = auto()


class ProvType(TcxStrEnum):
    LocalLan = auto()
    RemoteExt = auto()
    RemoteExtSipProxyMgr = auto()
    SBC = auto()


class PhoneDeviceVlanType(TcxStrEnum):
    Wan = auto()
    Pc = auto()


class XferTypeEnum(TcxStrEnum):
    BXfer = auto()
    AttXfer = auto()


class ProfileType(TcxStrEnum):
    Default = auto()
    Available = auto()
    Away = auto()
    OutOfOffice = auto()
    Available2 = auto()
    OutOfOffice2 = auto()


class DnType(TcxStrEnum):
    NONE = auto()
    Extension = auto()
    Queue = auto()
    RingGroup = auto()
    IVR = auto()
    Fax = auto()
    Conference = auto()
    Parking = auto()
    ExternalLine = auto()
    SpecialMenu = auto()


class VMEmailOptionsType(TcxStrEnum):
    NONE = auto()
    Notification = auto()
    Attachment = auto()
    AttachmentAndDelete = auto()


class VMPlayMsgDateTimeType(TcxStrEnum):
    NONE = auto()
    Play12Hr = auto()
    Play24Hr = auto()

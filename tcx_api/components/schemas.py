from enum import StrEnum, auto, EnumMeta
from typing import List


class TcxStrEnumMeta(EnumMeta):
    # StrEnum from 3CX can contain teh word None which we can't use in Python
    # So, we use NONE instead. This metaclass makes it so looking for None
    # returns the value for NONE instead.
    def __getitem__(self, name):
        if name == "None":
            name = "NONE"
        return super().__getitem__(name).value


class TcxStrEnum(StrEnum, metaclass=TcxStrEnumMeta):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        if name == "NONE":
            return "None"
        return name


class Pbx_RuleHoursType(TcxStrEnum):
    AllHours = auto()
    OfficeHours = auto()
    OutOfOfficeHours = auto()
    SpecificHours = auto()
    SpecificHoursExcludingHolidays = auto()
    OutOfSpecificHours = auto()
    OutOfSpecificHoursIncludingHolidays = auto()
    Never = auto()
    BreakTime = auto()


class Pbx_DayOfWeek(TcxStrEnum):
    Sunday = auto()
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()


class Pbx_Period:
    def __init__(
        self, DayOfWeek: Pbx_DayOfWeek = None, Start: str = None, Stop: str = None
    ) -> None:
        self.DayOfWeek = DayOfWeek
        self.Start = Start
        self.Stop = Stop


class Pbx_Schedule:
    def __init__(
        self,
        Type: Pbx_RuleHoursType,
        IgnoreHolidays: bool = None,
        Periods: list[Pbx_Period] = None,
    ) -> None:
        self.Type = Type
        self.IgnoreHolidays = IgnoreHolidays
        self.Periods = Periods


class Pbx_ScheduleType(TcxStrEnum):
    Daily = auto()
    Weekly = auto()
    Monthly = auto()
    Hourly = auto()
    Immediate = auto()


class Pbx_Authentication(TcxStrEnum):
    Both = auto()
    Name = auto()
    Email = auto()
    NONE = auto()


class Pbx_PeerType(TcxStrEnum):
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


class Pbx_DestinationType:
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


class Pbx_Destination:
    def __init__(
        self,
        External: str = None,
        Name: str = None,
        Number: str = None,
        PeerType: Pbx_PeerType = None,
        To: Pbx_DestinationType = None,
    ):
        self.External = External
        self.Name = Name
        self.Number = Number
        self.PeerType = PeerType
        self.To = To


class Pbx_ExtensionRule:
    def __init__(
        self,
        Id: int,
        CallerId: str = None,
        Destination: Pbx_Destination = None,
        Hours: Pbx_Schedule = None,
    ):
        self.Id = Id
        self.CallerId = CallerId
        self.Destination = Destination
        self.Hours = Hours


class Pbx_AvailableRouting:
    pass


class Pbx_AwayRouting:
    pass


class Pbx_ForwardingProfile:
    def __init__(
        self,
        Id: int,
        AcceptMultipleCalls: bool = None,
        AvailableRoute: Pbx_AvailableRouting = None,
        AwayRoute: Pbx_AwayRouting = None,
        BlockPushCalls: bool = None,
        CustomMessage: str = None,
        CustomName: str = None,
        DisableRingGroupCalls: bool = None,
        Name: str = None,
        NoAnswerTimeout: int = None,
        OfficeHoursAutoQueueLogOut: bool = None,
        RingMyMobile: bool = None,
    ):
        self.Id = Id
        self.AcceptMultipleCalls = AcceptMultipleCalls
        self.AvailableRoute = AvailableRoute
        self.AwayRoute = AwayRoute
        self.BlockPushCalls = BlockPushCalls
        self.CustomMessage = CustomMessage
        self.CustomName = CustomName
        self.DisableRingGroupCalls = DisableRingGroupCalls
        self.Name = Name
        self.NoAnswerTimeout = NoAnswerTimeout
        self.OfficeHoursAutoQueueLogOut = OfficeHoursAutoQueueLogOut
        self.RingMyMobile = RingMyMobile


class Pbx_OfficeHoursBits(TcxStrEnum):
    GlobalSchedule = auto()
    AutoSwitchProfiles = auto()
    AutoQueueLogOut = auto()
    BlockOutboundCalls = auto()


class Pbx_Phone:
    pass


class Pbx_Greeting:
    pass


class Pbx_UserGroup:
    pass


class Pbx_UserTag:
    pass


class Pbx_VMEmailOptionsType:
    pass


class Pbx_VMPlayMsgDateTimeType:
    pass

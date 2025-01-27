from threecxapi.util import TcxStrEnum
from enum import auto


class IVRType(TcxStrEnum):
    Default = auto()
    CodeBased = auto()
    ScriptBased = auto()
    Wakeup = auto()


class PeerType(TcxStrEnum):
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
    Group = auto()
    RoutePoint = auto()


class IVRForwardType(TcxStrEnum):
    EndCall = auto()
    Extension = auto()
    RingGroup = auto()
    Queue = auto()
    IVR = auto()
    VoiceMail = auto()
    CallByName = auto()
    RepeatPrompt = auto()
    CustomInput = auto()


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


class BlockType(TcxStrEnum):
    Block = auto()
    Allow = auto()


class AddedBy(TcxStrEnum):
    Manual = auto()
    Mcu = auto()
    Webmeeting = auto()
    AutoBlacklist = auto()
    Whitelist = auto()


class StrategyType(TcxStrEnum):
    Hunt = auto()
    RingAll = auto()
    Paging = auto()


class Authentication(TcxStrEnum):
    Both = auto()
    Name = auto()
    Email = auto()
    NONE = auto()


class PollingStrategyType(TcxStrEnum):
    Hunt = auto()
    RingAll = auto()
    HuntRandomStart = auto()
    NextAgent = auto()
    LongestWaiting = auto()
    LeastTalkTime = auto()
    FewestAnswered = auto()
    HuntBy3s = auto()
    First3Available = auto()
    SkillBasedRouting_RingAll = auto()
    SkillBasedRouting_HuntRandomStart = auto()
    SkillBasedRouting_RoundRobin = auto()
    SkillBasedRouting_FewestAnswered = auto()


class TypeOfChatOwnershipType(TcxStrEnum):
    TakeManually = auto()
    AutoAssign = auto()


class QueueRecording(TcxStrEnum):
    Disabled = auto()
    AllowToOptOut = auto()
    AskToOptIn = auto()


class QueueNotifyCode(TcxStrEnum):
    Callback = auto()
    CallbackFail = auto()
    SLATimeBreached = auto()
    CallLost = auto()


class ResetQueueStatisticsFrequency(TcxStrEnum):
    Disabled = auto()
    Daily = auto()
    Weekly = auto()
    Monthly = auto()


class DayOfWeek(TcxStrEnum):
    Sunday = auto()
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()


class VMEmailOptionsType(TcxStrEnum):
    NONE = auto()
    Notification = auto()
    Attachment = auto()
    AttachmentAndDelete = auto()


class VMPlayMsgDateTimeType(TcxStrEnum):
    NONE = auto()
    Play12Hr = auto()
    Play24Hr = auto()


class ProfileType(TcxStrEnum):
    Default = auto()
    Available = auto()
    Away = auto()
    OutOfOffice = auto()
    Available2 = auto()
    OutOfOffice2 = auto()


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


class OfficeHoursBits(TcxStrEnum):
    GlobalSchedule = auto()
    AutoSwitchProfiles = auto()
    AutoQueueLogOut = auto()
    BlockOutboundCalls = auto()


class ProvType(TcxStrEnum):
    LocalLan = auto()
    RemoteExt = auto()
    RemoteExtSipProxyMgr = auto()
    SBC = auto()


class XferTypeEnum(TcxStrEnum):
    BXfer = auto()
    AttXfer = auto()


class PhoneDeviceVlanType(TcxStrEnum):
    Wan = auto()
    Pc = auto()


class UserTag(TcxStrEnum):
    MS = auto()
    Teams = auto()
    Google = auto()
    WakeUp = auto()


class TemplateType(TcxStrEnum):
    Preferred = auto()
    Supported = auto()
    Dedicated = auto()
    ThirdParty = auto()
    Deleted = auto()
    Unknown = auto()


class TrunkEditorType(TcxStrEnum):
    Messaging = auto()
    Voip = auto()


class TrunkVariableType(TcxStrEnum):
    Text = auto()
    Password = auto()


class RecordingCallType(TcxStrEnum):
    Local = auto()
    InboundExternal = auto()
    OutboundExternal = auto()


class ScheduleType(TcxStrEnum):
    Daily = auto()
    Weekly = auto()
    Monthly = auto()
    Hourly = auto()
    Immediate = auto()


class FileSystemType(TcxStrEnum):
    Local = auto()
    Ftp = auto()
    GoogleDrive = auto()
    NetworkShare = auto()
    Logs = auto()
    Sftp = auto()
    GoogleBucket = auto()
    SharePoint = auto()


class CallHandlingFlags(TcxStrEnum):
    WelcomeMessageForIncomingCalls = auto()
    HoldCall = auto()


class GroupHoursMode(TcxStrEnum):
    Default = auto()
    ForceOpened = auto()
    ForceClosed = auto()
    ForceBreak = auto()
    ForceCustomOperator = auto()
    ForceHoliday = auto()
    HasForcedMask = auto()


class StartupLicense(TcxStrEnum):
    Free = auto()
    Pro = auto()


class DirectionType(TcxStrEnum):
    NONE = auto()
    Inbound = auto()
    Outbound = auto()
    Both = auto()


class SRTPModeType(TcxStrEnum):
    SRTPDisabled = auto()
    SRTPEnabled = auto()
    SRTPEnforced = auto()


class MatchingStrategyType(TcxStrEnum):
    MatchAnyFields = auto()
    MatchAllFields = auto()


class RequireRegistrationForType(TcxStrEnum):
    Nothing = auto()
    IncomingCalls = auto()
    OutgoingCalls = auto()
    InOutCalls = auto()


class GatewayType(TcxStrEnum):
    Unknown = auto()
    Analog = auto()
    Provider = auto()
    BridgeMaster = auto()
    BridgeSlave = auto()
    BridgeSlaveOverTunnel = auto()
    BRI = auto()
    T1 = auto()
    E1 = auto()


class IPInRegistrationContactType(TcxStrEnum):
    External = auto()
    Internal = auto()
    Both = auto()
    Specified = auto()


class RuleCallTypeType(TcxStrEnum):
    AllCalls = auto()
    InternalCallsOnly = auto()
    ExternalCallsOnly = auto()


class RuleConditionType(TcxStrEnum):
    NoAnswer = auto()
    PhoneBusy = auto()
    PhoneNotRegistered = auto()
    ForwardAll = auto()
    BasedOnCallerID = auto()
    BasedOnDID = auto()


class TypeOfIPDestriction(TcxStrEnum):
    Any = auto()
    IPV4 = auto()
    IPV6 = auto()


class TypeOfTransportRestriction(TcxStrEnum):
    Any = auto()
    UDP = auto()
    TCP = auto()
    TLS = auto()


class DeviceType(TcxStrEnum):
    Fxs = auto()
    Dect = auto()


class PromptSetType(TcxStrEnum):
    System = auto()
    Custom = auto()


class PromptType(TcxStrEnum):
    File = auto()
    Playlist = auto()


class AnimationStyle(TcxStrEnum):
    SlideUp = auto()
    SlideFromSide = auto()
    FadeIn = auto()
    NoAnimation = auto()


class LiveChatGreeting(TcxStrEnum):
    Disabled = auto()
    OnlyOnDesktop = auto()
    OnlyOnMobile = auto()
    DesktopAndMobile = auto()


class LiveChatCommunication(TcxStrEnum):
    ChatOnly = auto()
    PhoneAndChat = auto()
    PhoneOnly = auto()
    VideoPhoneAndChat = auto()


class LiveChatMinimizedStyle(TcxStrEnum):
    BubbleLeft = auto()
    BubbleRight = auto()
    BottomLeft = auto()
    BottomRight = auto()


class LiveChatLanguage(TcxStrEnum):
    browser = auto()
    en = auto()
    es = auto()
    de = auto()
    fr = auto()
    it = auto()
    pl = auto()
    ru = auto()
    pt = auto()
    zh = auto()


class LiveMessageUserinfoFormat(TcxStrEnum):
    Avatar = auto()
    Name = auto()
    Both = auto()
    NONE = auto()


class LiveChatMessageDateformat(TcxStrEnum):
    Date = auto()
    Time = auto()
    Both = auto()


class ButtonIconType(TcxStrEnum):
    Url = auto()
    Default = auto()
    Bubble = auto()
    DoubleBubble = auto()


class UpdateType(TcxStrEnum):
    Release = auto()
    Beta = auto()
    MajorRelease = auto()
    Alpha = auto()
    Hotfix = auto()


class FailoverMode(TcxStrEnum):
    Active = auto()
    Passive = auto()


class FailoverCondition(TcxStrEnum):
    AllService = auto()
    AnyService = auto()


class ChatType(TcxStrEnum):
    SMS = auto()
    LiveChat = auto()
    Facebook = auto()
    Internal = auto()
    RCS = auto()


class ParameterType(TcxStrEnum):
    String = auto()
    Integer = auto()
    Double = auto()
    Boolean = auto()
    DateTime = auto()
    Password = auto()
    OAuth = auto()
    List = auto()


class EditorType(TcxStrEnum):
    String = auto()
    Sql = auto()


class AuthenticationType(TcxStrEnum):
    No = auto()
    Basic = auto()
    Scenario = auto()


class TypeOfCDRLog(TcxStrEnum):
    SingleFileForAllCalls = auto()
    SingleFileForEachCall = auto()
    PassiveSocket = auto()
    ActiveSocket = auto()


class EventLogType(TcxStrEnum):
    Error = auto()
    Warning = auto()
    Info = auto()


class ServiceStatus(TcxStrEnum):
    Stopped = auto()
    StartPending = auto()
    StopPending = auto()
    Running = auto()
    ContinuePending = auto()
    PausePending = auto()
    Paused = auto()


class IntegrationSyncType(TcxStrEnum):
    SyncAllUsers = auto()
    SyncAllUsersExceptSelected = auto()
    SyncSelected = auto()


class TypeOfUser(TcxStrEnum):
    Users = auto()
    SharedMailboxes = auto()
    LicensedUsers = auto()


class TranscriptionLevel(TcxStrEnum):
    VoicemailsOnly = auto()
    RecordingsOnly = auto()
    Both = auto()


class MailServerType(TcxStrEnum):
    Tcx = auto()
    MS365 = auto()
    Custom = auto()


class PmsIntegrationType(TcxStrEnum):
    tcxpms = auto()
    fidelio = auto()


class SplitDNSConversionState(TcxStrEnum):
    NotDefined = auto()
    ConversionTriggered = auto()
    ConversionInProgress = auto()
    ConversionFinished = auto()


class XOperatingSystemType(TcxStrEnum):
    Other = auto()
    Linux = auto()
    Windows = auto()


class TypeOfAutoPickupForward(TcxStrEnum):
    TransferBack = auto()
    DN = auto()
    ExtensionVoiceMail = auto()
    ExternalNumber = auto()
    RoutePoint = auto()


class TypeOfPhoneBookResolving(TcxStrEnum):
    NotResolve = auto()
    MatchExact = auto()
    MatchLength = auto()


class TypeOfPhoneBookDisplay(TcxStrEnum):
    FirstNameLastName = auto()
    LastNameFirstName = auto()


class TypeOfPhoneBookAddQueueName(TcxStrEnum):
    NotAdd = auto()
    Append = auto()
    Prepend = auto()


class ChatRecipientsType(TcxStrEnum):
    NONE = auto()
    MyGroupManagers = auto()
    MyGroupAllMembers = auto()
    AllGroupsManagers = auto()


class PhonebookPriorityOptions(TcxStrEnum):
    NotQueryIfInPhonebookFound = auto()
    AlwaysQuery = auto()


class ContactType(TcxStrEnum):
    Company = auto()
    Personal = auto()


class ReferenceNumeric(TcxStrEnum):
    NEGATIVE_INF = "NEGATIVE_INFINITY"
    INF = "INFINITY"
    NaN = "NAN"

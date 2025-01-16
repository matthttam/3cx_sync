from tcx_api.components.response import Response
from pydantic import Field
from tcx_api.components.schemas.pbx import (
    Receptionist,
    BlackListNumber,
    BlocklistAddr,
    RingGroup,
    Contact,
    Queue,
    User,
    PhoneTemplate,
    TrunkTemplate,
    Recording,
    Group,
    OutboundRule,
    Parameter,
    DNProperty,
    Peer,
    Trunk,
    InboundRule,
    Country,
    Fxs,
    PromptSet,
    CustomPrompt,
    Property,
    FxsTemplate,
    Weblink,
    Parking,
    Backups,
    Sbc,
    CallHistoryView,
    ChatHistoryView,
    ChatMessagesHistoryView,
    RingGroupStatistics,
    ExtensionsStatisticsByRingGroups,
    CallLogData,
    RegistrarFxs,
    ExtensionStatistics,
    ReportExtensionStatisticsByGroup,
    CallCostByExtensionGroup,
    QueuePerformanceOverview,
    QueuePerformanceTotals,
    TeamQueueGeneralStatistics,
    DetailedQueueStatistics,
    AbandonedQueueCalls,
    QueueAnsweredCallsByWaitTime,
    QueueCallbacks,
    AgentsInQueueStatistics,
    QueueFailedCallbacks,
    StatisticSla,
    BreachesSla,
    CallFlowApp,
    QueueChatPerformance,
    QueueAgentsChatStatistics,
    QueueAgentsChatStatisticsTotals,
    AbandonedChatsStatistics,
    AgentLoginHistory,
    AuditLog,
    InboundRuleReport,
    CrmTemplate,
    CallCostSettings,
    PhoneLogo,
    TimeReportData,
    ReportGroup,
    EventLog,
    ServiceInfo,
    EmailTemplate,
    Playlist,
    Fax,
    DeviceInfo,
    SipDevice,
    NetworkInterface,
    ReceptionistForward,
    UserGroup,
    RingGroupMember,
    QueueAgent,
    QueueManager,
    Greeting,
    ForwardingProfile,
    ExtensionRule,
    Phone,
    Rights,
    Holiday,
    PeerGroup,
    Prompt,
    Codec,
    GatewayParameter,
    TimeZone,
    GatewayParameterValue,
    CrmSelectableValue,
    PhoneModel,
    OutboundRoute,
    DNRange,
    CIDFormatting,
    SetRoute,
    KeyValuePair_2OfString_String,
    DeviceLine,
    Variable,
    FxsModel,
    FxsVariable,
    UpdateItem,
    CategoryUpdate,
    CrmParameter,
    CDRSettingsField,
    Microsoft365User,
    GatewayParameterBinding,
    Choice,
    PhoneDeviceVlanInfo,
    CustomQueueRingtone,
    CrmChoice,
    CrmContact,
    Period,
    TrunkVariable,
    FxsVariableChoice,
)


class ReceptionistCollectionResponse(Response):
    value: list[Receptionist] = Field(default_factory=list)


class BlackListNumberCollectionResponse(Response):
    value: list[BlackListNumber] = Field(default_factory=list)


class BlocklistAddrCollectionResponse(Response):
    value: list[BlocklistAddr] = Field(default_factory=list)


class RingGroupCollectionResponse(Response):
    value: list[RingGroup] = Field(default_factory=list)


class ContactCollectionResponse(Response):
    value: list[Contact] = Field(default_factory=list)


class QueueCollectionResponse(Response):
    value: list[Queue] = Field(default_factory=list)


class UserCollectionResponse(Response):
    value: list[User] = Field(default_factory=list)


class PhoneTemplateCollectionResponse(Response):
    value: list[PhoneTemplate] = Field(default_factory=list)


class TrunkTemplateCollectionResponse(Response):
    value: list[TrunkTemplate] = Field(default_factory=list)


class RecordingCollectionResponse(Response):
    value: list[Recording] = Field(default_factory=list)


class GroupCollectionResponse(Response):
    value: list[Group] = Field(default_factory=list)


class OutboundRuleCollectionResponse(Response):
    value: list[OutboundRule] = Field(default_factory=list)


class ParameterCollectionResponse(Response):
    value: list[Parameter] = Field(default_factory=list)


class DNPropertyCollectionResponse(Response):
    value: list[DNProperty] = Field(default_factory=list)


class PeerCollectionResponse(Response):
    value: list[Peer] = Field(default_factory=list)


class TrunkCollectionResponse(Response):
    value: list[Trunk] = Field(default_factory=list)


class InboundRuleCollectionResponse(Response):
    value: list[InboundRule] = Field(default_factory=list)


class CountryCollectionResponse(Response):
    value: list[Country] = Field(default_factory=list)


class FxsCollectionResponse(Response):
    value: list[Fxs] = Field(default_factory=list)


class PromptSetCollectionResponse(Response):
    value: list[PromptSet] = Field(default_factory=list)


class CustomPromptCollectionResponse(Response):
    value: list[CustomPrompt] = Field(default_factory=list)


class PropertyCollectionResponse(Response):
    value: list[Property] = Field(default_factory=list)


class FxsTemplateCollectionResponse(Response):
    value: list[FxsTemplate] = Field(default_factory=list)


class WeblinkCollectionResponse(Response):
    value: list[Weblink] = Field(default_factory=list)


class ParkingCollectionResponse(Response):
    value: list[Parking] = Field(default_factory=list)


class BackupsCollectionResponse(Response):
    value: list[Backups] = Field(default_factory=list)


class SbcCollectionResponse(Response):
    value: list[Sbc] = Field(default_factory=list)


class CallHistoryViewCollectionResponse(Response):
    value: list[CallHistoryView] = Field(default_factory=list)


class ChatHistoryViewCollectionResponse(Response):
    value: list[ChatHistoryView] = Field(default_factory=list)


class ChatMessagesHistoryViewCollectionResponse(Response):
    value: list[ChatMessagesHistoryView] = Field(default_factory=list)


class RingGroupStatisticsCollectionResponse(Response):
    value: list[RingGroupStatistics] = Field(default_factory=list)


class ExtensionsStatisticsByRingGroupsCollectionResponse(Response):
    value: list[ExtensionsStatisticsByRingGroups] = Field(
        default_factory=list)


class CallLogDataCollectionResponse(Response):
    value: list[CallLogData] = Field(default_factory=list)


class RegistrarFxsCollectionResponse(Response):
    value: list[RegistrarFxs] = Field(default_factory=list)


class ExtensionStatisticsCollectionResponse(Response):
    value: list[ExtensionStatistics] = Field(default_factory=list)


class ReportExtensionStatisticsByGroupCollectionResponse(Response):
    value: list[ReportExtensionStatisticsByGroup] = Field(
        default_factory=list)


class CallCostByExtensionGroupCollectionResponse(Response):
    value: list[CallCostByExtensionGroup] = Field(default_factory=list)


class QueuePerformanceOverviewCollectionResponse(Response):
    value: list[QueuePerformanceOverview] = Field(default_factory=list)


class QueuePerformanceTotalsCollectionResponse(Response):
    value: list[QueuePerformanceTotals] = Field(default_factory=list)


class TeamQueueGeneralStatisticsCollectionResponse(Response):
    value: list[TeamQueueGeneralStatistics] = Field(default_factory=list)


class DetailedQueueStatisticsCollectionResponse(Response):
    value: list[DetailedQueueStatistics] = Field(default_factory=list)


class AbandonedQueueCallsCollectionResponse(Response):
    value: list[AbandonedQueueCalls] = Field(default_factory=list)


class QueueAnsweredCallsByWaitTimeCollectionResponse(Response):
    value: list[QueueAnsweredCallsByWaitTime] = Field(default_factory=list)


class QueueCallbacksCollectionResponse(Response):
    value: list[QueueCallbacks] = Field(default_factory=list)


class AgentsInQueueStatisticsCollectionResponse(Response):
    value: list[AgentsInQueueStatistics] = Field(default_factory=list)


class QueueFailedCallbacksCollectionResponse(Response):
    value: list[QueueFailedCallbacks] = Field(default_factory=list)


class StatisticSlaCollectionResponse(Response):
    value: list[StatisticSla] = Field(default_factory=list)


class BreachesSlaCollectionResponse(Response):
    value: list[BreachesSla] = Field(default_factory=list)


class CallFlowAppCollectionResponse(Response):
    value: list[CallFlowApp] = Field(default_factory=list)


class QueueChatPerformanceCollectionResponse(Response):
    value: list[QueueChatPerformance] = Field(default_factory=list)


class QueueAgentsChatStatisticsCollectionResponse(Response):
    value: list[QueueAgentsChatStatistics] = Field(default_factory=list)


class QueueAgentsChatStatisticsTotalsCollectionResponse(Response):
    value: list[QueueAgentsChatStatisticsTotals] = Field(
        default_factory=list)


class AbandonedChatsStatisticsCollectionResponse(Response):
    value: list[AbandonedChatsStatistics] = Field(default_factory=list)


class AgentLoginHistoryCollectionResponse(Response):
    value: list[AgentLoginHistory] = Field(default_factory=list)


class AuditLogCollectionResponse(Response):
    value: list[AuditLog] = Field(default_factory=list)


class InboundRuleReportCollectionResponse(Response):
    value: list[InboundRuleReport] = Field(default_factory=list)


class CrmTemplateCollectionResponse(Response):
    value: list[CrmTemplate] = Field(default_factory=list)


class CallCostSettingsCollectionResponse(Response):
    value: list[CallCostSettings] = Field(default_factory=list)


class PhoneLogoCollectionResponse(Response):
    value: list[PhoneLogo] = Field(default_factory=list)


class TimeReportDataCollectionResponse(Response):
    value: list[TimeReportData] = Field(default_factory=list)


class ReportGroupCollectionResponse(Response):
    value: list[ReportGroup] = Field(default_factory=list)


class EventLogCollectionResponse(Response):
    value: list[EventLog] = Field(default_factory=list)


class ServiceInfoCollectionResponse(Response):
    value: list[ServiceInfo] = Field(default_factory=list)


class EmailTemplateCollectionResponse(Response):
    value: list[EmailTemplate] = Field(default_factory=list)


class PlaylistCollectionResponse(Response):
    value: list[Playlist] = Field(default_factory=list)


class FaxCollectionResponse(Response):
    value: list[Fax] = Field(default_factory=list)


class DeviceInfoCollectionResponse(Response):
    value: list[DeviceInfo] = Field(default_factory=list)


class SipDeviceCollectionResponse(Response):
    value: list[SipDevice] = Field(default_factory=list)


class NetworkInterfaceCollectionResponse(Response):
    value: list[NetworkInterface] = Field(default_factory=list)


class ReceptionistForwardCollectionResponse(Response):
    value: list[ReceptionistForward] = Field(default_factory=list)


class UserGroupCollectionResponse(Response):
    value: list[UserGroup] = Field(default_factory=list)


class RingGroupMemberCollectionResponse(Response):
    value: list[RingGroupMember] = Field(default_factory=list)


class QueueAgentCollectionResponse(Response):
    value: list[QueueAgent] = Field(default_factory=list)


class QueueManagerCollectionResponse(Response):
    value: list[QueueManager] = Field(default_factory=list)


class GreetingCollectionResponse(Response):
    value: list[Greeting] = Field(default_factory=list)


class ForwardingProfileCollectionResponse(Response):
    value: list[ForwardingProfile] = Field(default_factory=list)


class ExtensionRuleCollectionResponse(Response):
    value: list[ExtensionRule] = Field(default_factory=list)


class PhoneCollectionResponse(Response):
    value: list[Phone] = Field(default_factory=list)


class RightsCollectionResponse(Response):
    value: list[Rights] = Field(default_factory=list)


class HolidayCollectionResponse(Response):
    value: list[Holiday] = Field(default_factory=list)


class PeerGroupCollectionResponse(Response):
    value: list[PeerGroup] = Field(default_factory=list)


class PromptCollectionResponse(Response):
    value: list[Prompt] = Field(default_factory=list)


class CodecCollectionResponse(Response):
    value: list[Codec] = Field(default_factory=list)


class GatewayParameterCollectionResponse(Response):
    value: list[GatewayParameter] = Field(default_factory=list)


class TimeZoneCollectionResponse(Response):
    value: list[TimeZone] = Field(default_factory=list)


class GatewayParameterValueCollectionResponse(Response):
    value: list[GatewayParameterValue] = Field(default_factory=list)


class CrmSelectableValueCollectionResponse(Response):
    value: list[CrmSelectableValue] = Field(default_factory=list)


class PhoneModelCollectionResponse(Response):
    value: list[PhoneModel] = Field(default_factory=list)


class OutboundRouteCollectionResponse(Response):
    value: list[OutboundRoute] = Field(default_factory=list)


class DNRangeCollectionResponse(Response):
    value: list[DNRange] = Field(default_factory=list)


class CIDFormattingCollectionResponse(Response):
    value: list[CIDFormatting] = Field(default_factory=list)


class SetRouteCollectionResponse(Response):
    value: list[SetRoute] = Field(default_factory=list)


class KeyValuePair_2OfString_StringCollectionResponse(Response):
    value: list[KeyValuePair_2OfString_String] = Field(default_factory=list)


class DeviceLineCollectionResponse(Response):
    value: list[DeviceLine] = Field(default_factory=list)


class VariableCollectionResponse(Response):
    value: list[Variable] = Field(default_factory=list)


class FxsModelCollectionResponse(Response):
    value: list[FxsModel] = Field(default_factory=list)


class FxsVariableCollectionResponse(Response):
    value: list[FxsVariable] = Field(default_factory=list)


class UpdateItemCollectionResponse(Response):
    value: list[UpdateItem] = Field(default_factory=list)


class CategoryUpdateCollectionResponse(Response):
    value: list[CategoryUpdate] = Field(default_factory=list)


class CrmParameterCollectionResponse(Response):
    value: list[CrmParameter] = Field(default_factory=list)


class CDRSettingsFieldCollectionResponse(Response):
    value: list[CDRSettingsField] = Field(default_factory=list)


class Microsoft365UserCollectionResponse(Response):
    value: list[Microsoft365User] = Field(default_factory=list)


class GatewayParameterBindingCollectionResponse(Response):
    value: list[GatewayParameterBinding] = Field(default_factory=list)


class ChoiceCollectionResponse(Response):
    value: list[Choice] = Field(default_factory=list)


class PhoneDeviceVlanInfoCollectionResponse(Response):
    value: list[PhoneDeviceVlanInfo] = Field(default_factory=list)


class CustomQueueRingtoneCollectionResponse(Response):
    value: list[CustomQueueRingtone] = Field(default_factory=list)


class CrmChoiceCollectionResponse(Response):
    value: list[CrmChoice] = Field(default_factory=list)


class CrmContactCollectionResponse(Response):
    value: list[CrmContact] = Field(default_factory=list)


class PeriodCollectionResponse(Response):
    value: list[Period] = Field(default_factory=list)


class TrunkVariableCollectionResponse(Response):
    value: list[TrunkVariable] = Field(default_factory=list)


class FxsVariableChoiceCollectionResponse(Response):
    value: list[FxsVariableChoice] = Field(default_factory=list)

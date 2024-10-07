from tcx_api.components.schemas.pbx import *
from tcx_api.components.response import Response


class ReceptionistCollectionResponse(Response):
    value: conlist(Receptionist) = Field(default_factory=list)


class BlackListNumberCollectionResponse(Response):
    value: conlist(BlackListNumber) = Field(default_factory=list)


class BlocklistAddrCollectionResponse(Response):
    value: conlist(BlocklistAddr) = Field(default_factory=list)


class RingGroupCollectionResponse(Response):
    value: conlist(RingGroup) = Field(default_factory=list)


class ContactCollectionResponse(Response):
    value: conlist(Contact) = Field(default_factory=list)


class QueueCollectionResponse(Response):
    value: conlist(Queue) = Field(default_factory=list)


class UserCollectionResponse(Response):
    value: conlist(User) = Field(default_factory=list)


class PhoneTemplateCollectionResponse(Response):
    value: conlist(PhoneTemplate) = Field(default_factory=list)


class TrunkTemplateCollectionResponse(Response):
    value: conlist(TrunkTemplate) = Field(default_factory=list)


class RecordingCollectionResponse(Response):
    value: conlist(Recording) = Field(default_factory=list)


class GroupCollectionResponse(Response):
    value: conlist(Group) = Field(default_factory=list)


class OutboundRuleCollectionResponse(Response):
    value: conlist(OutboundRule) = Field(default_factory=list)


class ParameterCollectionResponse(Response):
    value: conlist(Parameter) = Field(default_factory=list)


class DNPropertyCollectionResponse(Response):
    value: conlist(DNProperty) = Field(default_factory=list)


class PeerCollectionResponse(Response):
    value: conlist(Peer) = Field(default_factory=list)


class TrunkCollectionResponse(Response):
    value: conlist(Trunk) = Field(default_factory=list)


class InboundRuleCollectionResponse(Response):
    value: conlist(InboundRule) = Field(default_factory=list)


class CountryCollectionResponse(Response):
    value: conlist(Country) = Field(default_factory=list)


class FxsCollectionResponse(Response):
    value: conlist(Fxs) = Field(default_factory=list)


class PromptSetCollectionResponse(Response):
    value: conlist(PromptSet) = Field(default_factory=list)


class CustomPromptCollectionResponse(Response):
    value: conlist(CustomPrompt) = Field(default_factory=list)


class PropertyCollectionResponse(Response):
    value: conlist(Property) = Field(default_factory=list)


class FxsTemplateCollectionResponse(Response):
    value: conlist(FxsTemplate) = Field(default_factory=list)


class WeblinkCollectionResponse(Response):
    value: conlist(Weblink) = Field(default_factory=list)


class ParkingCollectionResponse(Response):
    value: conlist(Parking) = Field(default_factory=list)


class BackupsCollectionResponse(Response):
    value: conlist(Backups) = Field(default_factory=list)


class SbcCollectionResponse(Response):
    value: conlist(Sbc) = Field(default_factory=list)


class CallHistoryViewCollectionResponse(Response):
    value: conlist(CallHistoryView) = Field(default_factory=list)


class ChatHistoryViewCollectionResponse(Response):
    value: conlist(ChatHistoryView) = Field(default_factory=list)


class ChatMessagesHistoryViewCollectionResponse(Response):
    value: conlist(ChatMessagesHistoryView) = Field(default_factory=list)


class RingGroupStatisticsCollectionResponse(Response):
    value: conlist(RingGroupStatistics) = Field(default_factory=list)


class ExtensionsStatisticsByRingGroupsCollectionResponse(Response):
    value: conlist(ExtensionsStatisticsByRingGroups) = Field(
        default_factory=list)


class CallLogDataCollectionResponse(Response):
    value: conlist(CallLogData) = Field(default_factory=list)


class RegistrarFxsCollectionResponse(Response):
    value: conlist(RegistrarFxs) = Field(default_factory=list)


class ExtensionStatisticsCollectionResponse(Response):
    value: conlist(ExtensionStatistics) = Field(default_factory=list)


class ReportExtensionStatisticsByGroupCollectionResponse(Response):
    value: conlist(ReportExtensionStatisticsByGroup) = Field(
        default_factory=list)


class CallCostByExtensionGroupCollectionResponse(Response):
    value: conlist(CallCostByExtensionGroup) = Field(default_factory=list)


class QueuePerformanceOverviewCollectionResponse(Response):
    value: conlist(QueuePerformanceOverview) = Field(default_factory=list)


class QueuePerformanceTotalsCollectionResponse(Response):
    value: conlist(QueuePerformanceTotals) = Field(default_factory=list)


class TeamQueueGeneralStatisticsCollectionResponse(Response):
    value: conlist(TeamQueueGeneralStatistics) = Field(default_factory=list)


class DetailedQueueStatisticsCollectionResponse(Response):
    value: conlist(DetailedQueueStatistics) = Field(default_factory=list)


class AbandonedQueueCallsCollectionResponse(Response):
    value: conlist(AbandonedQueueCalls) = Field(default_factory=list)


class QueueAnsweredCallsByWaitTimeCollectionResponse(Response):
    value: conlist(QueueAnsweredCallsByWaitTime) = Field(default_factory=list)


class QueueCallbacksCollectionResponse(Response):
    value: conlist(QueueCallbacks) = Field(default_factory=list)


class AgentsInQueueStatisticsCollectionResponse(Response):
    value: conlist(AgentsInQueueStatistics) = Field(default_factory=list)


class QueueFailedCallbacksCollectionResponse(Response):
    value: conlist(QueueFailedCallbacks) = Field(default_factory=list)


class StatisticSlaCollectionResponse(Response):
    value: conlist(StatisticSla) = Field(default_factory=list)


class BreachesSlaCollectionResponse(Response):
    value: conlist(BreachesSla) = Field(default_factory=list)


class CallFlowAppCollectionResponse(Response):
    value: conlist(CallFlowApp) = Field(default_factory=list)


class QueueChatPerformanceCollectionResponse(Response):
    value: conlist(QueueChatPerformance) = Field(default_factory=list)


class QueueAgentsChatStatisticsCollectionResponse(Response):
    value: conlist(QueueAgentsChatStatistics) = Field(default_factory=list)


class QueueAgentsChatStatisticsTotalsCollectionResponse(Response):
    value: conlist(QueueAgentsChatStatisticsTotals) = Field(
        default_factory=list)


class AbandonedChatsStatisticsCollectionResponse(Response):
    value: conlist(AbandonedChatsStatistics) = Field(default_factory=list)


class AgentLoginHistoryCollectionResponse(Response):
    value: conlist(AgentLoginHistory) = Field(default_factory=list)


class AuditLogCollectionResponse(Response):
    value: conlist(AuditLog) = Field(default_factory=list)


class InboundRuleReportCollectionResponse(Response):
    value: conlist(InboundRuleReport) = Field(default_factory=list)


class CrmTemplateCollectionResponse(Response):
    value: conlist(CrmTemplate) = Field(default_factory=list)


class CallCostSettingsCollectionResponse(Response):
    value: conlist(CallCostSettings) = Field(default_factory=list)


class PhoneLogoCollectionResponse(Response):
    value: conlist(PhoneLogo) = Field(default_factory=list)


class TimeReportDataCollectionResponse(Response):
    value: conlist(TimeReportData) = Field(default_factory=list)


class ReportGroupCollectionResponse(Response):
    value: conlist(ReportGroup) = Field(default_factory=list)


class EventLogCollectionResponse(Response):
    value: conlist(EventLog) = Field(default_factory=list)


class ServiceInfoCollectionResponse(Response):
    value: conlist(ServiceInfo) = Field(default_factory=list)


class EmailTemplateCollectionResponse(Response):
    value: conlist(EmailTemplate) = Field(default_factory=list)


class PlaylistCollectionResponse(Response):
    value: conlist(Playlist) = Field(default_factory=list)


class FaxCollectionResponse(Response):
    value: conlist(Fax) = Field(default_factory=list)


class DeviceInfoCollectionResponse(Response):
    value: conlist(DeviceInfo) = Field(default_factory=list)


class SipDeviceCollectionResponse(Response):
    value: conlist(SipDevice) = Field(default_factory=list)


class NetworkInterfaceCollectionResponse(Response):
    value: conlist(NetworkInterface) = Field(default_factory=list)


class ReceptionistForwardCollectionResponse(Response):
    value: conlist(ReceptionistForward) = Field(default_factory=list)


class UserGroupCollectionResponse(Response):
    value: conlist(UserGroup) = Field(default_factory=list)


class RingGroupMemberCollectionResponse(Response):
    value: conlist(RingGroupMember) = Field(default_factory=list)


class QueueAgentCollectionResponse(Response):
    value: conlist(QueueAgent) = Field(default_factory=list)


class QueueManagerCollectionResponse(Response):
    value: conlist(QueueManager) = Field(default_factory=list)


class GreetingCollectionResponse(Response):
    value: conlist(Greeting) = Field(default_factory=list)


class ForwardingProfileCollectionResponse(Response):
    value: conlist(ForwardingProfile) = Field(default_factory=list)


class ExtensionRuleCollectionResponse(Response):
    value: conlist(ExtensionRule) = Field(default_factory=list)


class PhoneCollectionResponse(Response):
    value: conlist(Phone) = Field(default_factory=list)


class RightsCollectionResponse(Response):
    value: conlist(Rights) = Field(default_factory=list)


class HolidayCollectionResponse(Response):
    value: conlist(Holiday) = Field(default_factory=list)


class PeerGroupCollectionResponse(Response):
    value: conlist(PeerGroup) = Field(default_factory=list)


class PromptCollectionResponse(Response):
    value: conlist(Prompt) = Field(default_factory=list)


class CodecCollectionResponse(Response):
    value: conlist(Codec) = Field(default_factory=list)


class GatewayParameterCollectionResponse(Response):
    value: conlist(GatewayParameter) = Field(default_factory=list)


class TimeZoneCollectionResponse(Response):
    value: conlist(TimeZone) = Field(default_factory=list)


class GatewayParameterValueCollectionResponse(Response):
    value: conlist(GatewayParameterValue) = Field(default_factory=list)


class CrmSelectableValueCollectionResponse(Response):
    value: conlist(CrmSelectableValue) = Field(default_factory=list)


class PhoneModelCollectionResponse(Response):
    value: conlist(PhoneModel) = Field(default_factory=list)


class OutboundRouteCollectionResponse(Response):
    value: conlist(OutboundRoute) = Field(default_factory=list)


class DNRangeCollectionResponse(Response):
    value: conlist(DNRange) = Field(default_factory=list)


class CIDFormattingCollectionResponse(Response):
    value: conlist(CIDFormatting) = Field(default_factory=list)


class SetRouteCollectionResponse(Response):
    value: conlist(SetRoute) = Field(default_factory=list)


class KeyValuePair_2OfString_StringCollectionResponse(Response):
    value: conlist(KeyValuePair_2OfString_String) = Field(default_factory=list)


class DeviceLineCollectionResponse(Response):
    value: conlist(DeviceLine) = Field(default_factory=list)


class VariableCollectionResponse(Response):
    value: conlist(Variable) = Field(default_factory=list)


class FxsModelCollectionResponse(Response):
    value: conlist(FxsModel) = Field(default_factory=list)


class FxsVariableCollectionResponse(Response):
    value: conlist(FxsVariable) = Field(default_factory=list)


class UpdateItemCollectionResponse(Response):
    value: conlist(UpdateItem) = Field(default_factory=list)


class CategoryUpdateCollectionResponse(Response):
    value: conlist(CategoryUpdate) = Field(default_factory=list)


class CrmParameterCollectionResponse(Response):
    value: conlist(CrmParameter) = Field(default_factory=list)


class CDRSettingsFieldCollectionResponse(Response):
    value: conlist(CDRSettingsField) = Field(default_factory=list)


class Microsoft365UserCollectionResponse(Response):
    value: conlist(Microsoft365User) = Field(default_factory=list)


class GatewayParameterBindingCollectionResponse(Response):
    value: conlist(GatewayParameterBinding) = Field(default_factory=list)


class ChoiceCollectionResponse(Response):
    value: conlist(Choice) = Field(default_factory=list)


class PhoneDeviceVlanInfoCollectionResponse(Response):
    value: conlist(PhoneDeviceVlanInfo) = Field(default_factory=list)


class CustomQueueRingtoneCollectionResponse(Response):
    value: conlist(CustomQueueRingtone) = Field(default_factory=list)


class CrmChoiceCollectionResponse(Response):
    value: conlist(CrmChoice) = Field(default_factory=list)


class CrmContactCollectionResponse(Response):
    value: conlist(CrmContact) = Field(default_factory=list)


class PeriodCollectionResponse(Response):
    value: conlist(Period) = Field(default_factory=list)


class TrunkVariableCollectionResponse(Response):
    value: conlist(TrunkVariable) = Field(default_factory=list)


class FxsVariableChoiceCollectionResponse(Response):
    value: conlist(FxsVariableChoice) = Field(default_factory=list)

from tcx_api.components.schemas.pbx.available_routing import (
    AvailableRouting as AvailableRoutingObject,
)
from tcx_api.components.schemas.pbx.away_routing import AwayRouting as AwayRoutingObject
from tcx_api.components.schemas.schema import Schema


class ForwardingProfile(Schema):
    Id: int
    AcceptMultipleCalls: bool = None
    AvailableRoute: AvailableRoutingObject = None
    AwayRoute: AwayRoutingObject = None
    BlockPushCalls: bool = None
    CustomMessage: str = None
    CustomName: str = None
    DisableRingGroupCalls: bool = None
    Name: str = None
    NoAnswerTimeout: int = None
    OfficeHoursAutoQueueLogOut: bool = None
    RingMyMobile: bool = None

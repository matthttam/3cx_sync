from tcx_api.components.schemas.pbx.schemas import AvailableRouting, AwayRouting


class ForwardingProfile:
    def __init__(
        self,
        Id: int,
        AcceptMultipleCalls: bool = None,
        AvailableRoute: AvailableRouting = None,
        AwayRoute: AwayRouting = None,
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

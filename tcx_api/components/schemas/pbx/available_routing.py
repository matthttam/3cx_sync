from tcx_api.components.schemas.pbx.destination import Destination
from tcx_api.util.util import Util


class AvailableRouting:
    def __init__(
        self,
        BusyAllCalls: bool = None,
        BusyExternal: Destination | dict = None,
        BusyInternal: Destination | dict = None,
        NoAnswerAllCalls: bool = None,
        NoAnswerExternal: Destination | dict = None,
        NoRegistrationAllCalls: bool = None,
        NotRegisteredExternal: Destination | dict = None,
        NotRegisteredInternal: Destination | dict = None,
    ) -> None:
        self.BusyAllCalls = BusyAllCalls
        self.BusyExternal = Util.instanciate_object(BusyExternal, Destination)
        self.BusyInternal = Util.instanciate_object(BusyInternal, Destination)
        self.NoAnswerAllCalls = NoAnswerAllCalls
        self.NoAnswerExternal = Util.instanciate_object(NoAnswerExternal, Destination)
        self.NoRegistrationAllCalls = NoRegistrationAllCalls
        self.NotRegisteredExternal = Util.instanciate_object(
            NotRegisteredExternal, Destination
        )
        self.NotRegisteredInternal = Util.instanciate_object(
            NotRegisteredInternal, Destination
        )

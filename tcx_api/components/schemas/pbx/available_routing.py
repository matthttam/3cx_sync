from tcx_api.components.schemas.pbx.destination import Destination


from tcx_api.components.schemas.schema import Schema


class AvailableRouting(Schema):
    BusyAllCalls: bool = None
    BusyExternal: Destination = None
    BusyInternal: Destination = None
    NoAnswerAllCalls: bool = None
    NoAnswerExternal: Destination = None
    NoRegistrationAllCalls: bool = None
    NotRegisteredExternal: Destination = None
    NotRegisteredInternal: Destination = None

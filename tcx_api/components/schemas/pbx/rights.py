from tcx_api.components.schemas.schema import Schema


class Rights(Schema):
    RoleName: str
    AllowIVR: bool = None
    AllowParking: bool = None
    AllowToChangePresence: bool = None
    AllowToManageCompanyBook: bool = None
    AssignClearOperations: bool = None
    CanBargeIn: bool = None
    CanIntercom: bool = None
    CanSeeGroupCalls: bool = None
    CanSeeGroupMembers: bool = None
    CanSeeGroupRecordings: bool = None
    PerformOperations: bool = None
    ShowMyCalls: bool = None
    ShowMyPresence: bool = None
    ShowMyPresenceOutside: bool = None

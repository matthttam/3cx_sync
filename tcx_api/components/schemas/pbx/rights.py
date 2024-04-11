class Rights:
    def __init__(
        self,
        RoleName: str,
        AllowIVR: bool = None,
        AllowParking: bool = None,
        AllowToChangePresence: bool = None,
        AllowToManageCompanyBook: bool = None,
        AssignClearOperations: bool = None,
        CanBargeIn: bool = None,
        CanIntercom: bool = None,
        CanSeeGroupCalls: bool = None,
        CanSeeGroupMembers: bool = None,
        CanSeeGroupRecordings: bool = None,
        PerformOperations: bool = None,
        ShowMyCalls: bool = None,
        ShowMyPresence: bool = None,
        ShowMyPresenceOutside: bool = None,
    ) -> None:
        self.RoleName = RoleName
        self.AllowIVR = AllowIVR
        self.AllowParking = AllowParking
        self.AllowToChangePresence = AllowToChangePresence
        self.AllowToManageCompanyBook = AllowToManageCompanyBook
        self.AssignClearOperations = AssignClearOperations
        self.CanBargeIn = CanBargeIn
        self.CanIntercom = CanIntercom
        self.CanSeeGroupCalls = CanSeeGroupCalls
        self.CanSeeGroupMembers = CanSeeGroupMembers
        self.CanSeeGroupRecordings = CanSeeGroupRecordings
        self.PerformOperations = PerformOperations
        self.ShowMyCalls = ShowMyCalls
        self.ShowMyPresence = ShowMyPresence
        self.ShowMyPresenceOutside = ShowMyPresenceOutside

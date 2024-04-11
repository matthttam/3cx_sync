from tcx_api.components.schemas.pbx.rights import Rights
from tcx_api.components.schemas.pbx.enums import DnType


class UserGroup:
    def __init__(
        self,
        CanDelete: bool = None,
        GroupId: int = None,
        Id: int = None,
        MemberName: str = None,
        Name: str = None,
        Number: str = None,
        Rights: Rights = None,
        Type: DnType = None,
    ) -> None:
        self.CanDelete = CanDelete
        self.GroupId = GroupId
        self.Id = Id
        self.MemberName = MemberName
        self.Name = Name
        self.Number = Number
        self.Rights = Rights
        self.Type = Type

from tcx_api.components.schemas.pbx.rights import Rights as RightsObject
from tcx_api.components.schemas.pbx.enums import DnType as DnTypeEnum
from tcx_api.components.schemas.schema import Schema


class UserGroup(Schema):
    CanDelete: bool = None
    GroupId: int = None
    Id: int = None
    MemberName: str = None
    Name: str = None
    Number: str = None
    Rights: RightsObject = None
    Type: DnTypeEnum = None

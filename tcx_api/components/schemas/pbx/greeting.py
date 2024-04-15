from tcx_api.components.schemas.pbx.enums import ProfileType as ProfileTypeEnum
from tcx_api.components.schemas.schema import Schema


class Greeting(Schema):
    Type: ProfileTypeEnum
    DisplayName: str = None
    Filename: str = None

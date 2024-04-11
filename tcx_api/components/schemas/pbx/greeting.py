from tcx_api.components.schemas.pbx.enums import ProfileType
from tcx_api.util.util import Util


class Greeting:
    def __init__(
        self,
        Type: ProfileType | str,
        DisplayName: str = None,
        Filename: str = None,
    ) -> None:
        self.DisplayName = DisplayName
        self.Filename = Filename
        self.Type = Util.instanciate_str_enum(Type)

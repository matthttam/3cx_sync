from tcx_api.components.schemas.pbx.enums import (
    DestinationType as DestinationTypeEnum,
    PeerType as PeerTypeEnum,
)
from tcx_api.components.schemas.schema import Schema


class Destination(Schema):
    External: str = None
    Name: str = None
    Number: str = None
    PeerType: PeerTypeEnum = None
    To: DestinationTypeEnum = None

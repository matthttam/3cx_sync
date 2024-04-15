from tcx_api.components.schemas.pbx.enums import (
    PhoneDeviceVlanType as PhoneDeviceVlanTypeEnum,
)
from tcx_api.components.schemas.schema import Schema


class PhoneDeviceVlanInfo(Schema):
    Configurable: bool = None
    Enabled: bool = None
    Priority: int = None
    PriorityConfigurable: bool = None
    PriorityMax: int = None
    PriorityMin: int = None
    Type: PhoneDeviceVlanTypeEnum = None
    VlanId: int = None
    VlanIdMax: int = None
    VlanIdMin: int = None

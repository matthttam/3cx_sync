from tcx_api.components.schemas.pbx.enums import PhoneDeviceVlanType
from tcx_api.util import Util
from typing import List


class PhoneDeviceVlanInfo:
    def __init__(
        self,
        Configurable: bool = None,
        Enabled: bool = None,
        Priority: int = None,
        PriorityConfigurable: bool = None,
        PriorityMax: int = None,
        PriorityMin: int = None,
        Type: PhoneDeviceVlanType | str = None,
        VlanId: int = None,
        VlanIdMax: int = None,
        VlanIdMin: int = None,
    ) -> None:
        self.Configurable = Configurable
        self.Enabled = Enabled
        self.Priority = Priority
        self.PriorityConfigurable = PriorityConfigurable
        self.PriorityMax = PriorityMax
        self.PriorityMin = PriorityMin
        self.Type = Util.instanciate_str_enum(Type)
        self.VlanId = VlanId
        self.VlanIdMax = VlanIdMax
        self.VlanIdMin = VlanIdMin

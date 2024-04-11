from tcx_api.components.schemas.pbx.phone_settings import PhoneSettings
from tcx_api.util.util import Util


class Phone:
    def __init__(
        self,
        Id: int,
        Interface: str = None,
        MacAddress: str = None,
        Name: str = None,
        ProvisioningLinkExt: str = None,
        ProvisioningLinkLocal: str = None,
        Settings: PhoneSettings = None,
        TemplateName: str = None,
    ) -> None:
        self.Id = Id
        self.Interface = Interface
        self.MacAddress = MacAddress
        self.Name = Name
        self.ProvisioningLinkExt = ProvisioningLinkExt
        self.ProvisioningLinkLocal = ProvisioningLinkLocal
        self.Settings = Util.instanciate_object(Settings, PhoneSettings)
        self.TemplateName = TemplateName

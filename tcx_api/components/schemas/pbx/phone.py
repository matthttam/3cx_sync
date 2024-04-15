from tcx_api.components.schemas.pbx.phone_settings import PhoneSettings
from tcx_api.components.schemas.schema import Schema


class Phone(Schema):
    Id: int
    Interface: str = None
    MacAddress: str = None
    Name: str = None
    ProvisioningLinkExt: str = None
    ProvisioningLinkLocal: str = None
    Settings: PhoneSettings = None
    TemplateName: str = None

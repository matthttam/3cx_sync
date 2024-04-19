
from typing import Optional
from tcx_api.components.schemas.enums import *
from typing import Any


from tcx_api.components.schemas.pbx import Schema


class ReferenceUpdate(Schema):
    # '@odata.id': str = ''
    # '@odata.type': Optional[str]
    id: str
    type: Optional[str] = None


class ReferenceCreate(Schema):
    # '@odata.id': str
    id: str
    additionalProperties: Any


class ReplaceMyGroupLicenseKeyRequestBody(Schema):
    licenseKey: str


class LinkMyGroupPartnerRequestBody(Schema):
    resellerId: str


class Enable2FARequestBody(Schema):
    enable: bool = False
    code: str


class RegenerateRequestBody(Schema):
    SipAuth: bool = False
    WebclientPassword: bool = False
    VoicemailPIN: bool = False
    DeskphonePassword: bool = False
    SendWelcomeEmail: bool = False
    ConfigurationLink: bool = False
    RpsKey: bool = False


class MakeCallUserRecordGreetingRequestBody(Schema):
    dn: str
    filename: str


class SetMonitorStatusRequestBody(Schema):
    days: int

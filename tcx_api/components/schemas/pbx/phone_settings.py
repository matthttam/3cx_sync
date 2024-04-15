from tcx_api.components.schemas.pbx.custom_queue_ringtone import (
    CustomQueueRingtone as CustomQueueRingtoneObject,
)
from tcx_api.components.schemas.pbx.phone_lldp_info import (
    PhoneLldpInfo as PhoneLldpInfoObject,
)
from tcx_api.components.schemas.pbx.phone_device_vlan_info import (
    PhoneDeviceVlanInfo as PhoneDeviceVlanInfoObject,
)

from tcx_api.components.schemas.pbx.enums import ProvType, XferTypeEnum
from typing import List


from tcx_api.components.schemas.schema import Schema
from typing import List
from pydantic import conlist


class PhoneSettings(Schema):
    AllowCustomQueueRingtones: bool = None
    Backlight: str = None
    Codecs: conlist(str) = []
    CustomLogo: str = None
    CustomQueueRingtones: conlist(CustomQueueRingtoneObject) = []
    DateFormat: str = None
    Firmware: str = None
    FirmwareLang: str = None
    IsLogoCustomizable: bool = None
    IsSBC: bool = None
    LlDpInfo: PhoneLldpInfoObject | dict = None
    LocalRTPPortEnd: int = None
    LocalRTPPortStart: int = None
    LocalSipPort: int = None
    LogoDescription: str = None
    LogoFileExtensionAllowed: conlist(str) = []
    OwnBlfs: bool = None
    PhoneLanguage: str = None
    PowerLed: str = None
    ProvisionExtendedData: str = None
    ProvisionType: ProvType | str = None
    QueueRingTone: str = None
    RemoteSpmHost: str = None
    RemoteSpmPort: int = None
    RingTone: str = None
    SbcName: str = None
    ScreenSaver: str = None
    Secret: str = None
    Srtp: str = None
    TimeFormat: str = None
    TimeZone: str = None
    VlanInfos: conlist(PhoneDeviceVlanInfoObject) = []
    XferType: XferTypeEnum | str = None

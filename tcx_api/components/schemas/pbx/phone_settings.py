from tcx_api.factories.resource_factory import ResourceFactory
from tcx_api.components.schemas.pbx.custom_queue_ringtone import CustomQueueRingtone
from tcx_api.components.schemas.pbx.phone_lldp_info import PhoneLldpInfo
from tcx_api.components.schemas.pbx.phone_device_vlan_info import PhoneDeviceVlanInfo

from tcx_api.components.schemas.pbx.enums import ProvType, XferTypeEnum
from typing import List

from tcx_api.util.util import Util


class PhoneSettings:
    def __init__(
        self,
        AllowCustomQueueRingtones: bool = None,
        Backlight: str = None,
        Codecs: list[str] = [],
        CustomLogo: str = None,
        CustomQueueRingtones: list[CustomQueueRingtone] = [],
        DateFormat: str = None,
        Firmware: str = None,
        FirmwareLang: str = None,
        IsLogoCustomizable: bool = None,
        IsSBC: bool = None,
        LlDpInfo: PhoneLldpInfo = None,
        LocalRTPPortEnd: int = None,
        LocalRTPPortStart: int = None,
        LocalSipPort: int = None,
        LogoDescription: str = None,
        LogoFileExtensionAllowed: list[str] = [],
        OwnBlfs: bool = None,
        PhoneLanguage: str = None,
        PowerLed: str = None,
        ProvisionExtendedData: str = None,
        ProvisionType: ProvType | str = None,
        QueueRingTone: str = None,
        RemoteSpmHost: str = None,
        RemoteSpmPort: int = None,
        RingTone: str = None,
        SbcName: str = None,
        ScreenSaver: str = None,
        Secret: str = None,
        Srtp: str = None,
        TimeFormat: str = None,
        TimeZone: str = None,
        VlanInfos: list[PhoneDeviceVlanInfo] = [],
        XferType: XferTypeEnum | str = None,
    ) -> None:
        self.AllowCustomQueueRingtones = AllowCustomQueueRingtones
        self.Backlight = Backlight
        self.Codecs = Codecs
        self.CustomLogo = CustomLogo
        self.CustomQueueRingtones = CustomQueueRingtones
        self.DateFormat = DateFormat
        self.Firmware = Firmware
        self.FirmwareLang = FirmwareLang
        self.IsLogoCustomizable = IsLogoCustomizable
        self.IsSBC = IsSBC
        self.LlDpInfo = LlDpInfo
        self.LocalRTPPortEnd = LocalRTPPortEnd
        self.LocalRTPPortStart = LocalRTPPortStart
        self.LocalSipPort = LocalSipPort
        self.LogoDescription = LogoDescription
        self.LogoFileExtensionAllowed = LogoFileExtensionAllowed
        self.OwnBlfs = OwnBlfs
        self.PhoneLanguage = PhoneLanguage
        self.PowerLed = PowerLed
        self.ProvisionExtendedData = ProvisionExtendedData
        self.ProvisionType = ProvisionType
        self.QueueRingTone = QueueRingTone
        self.RemoteSpmHost = RemoteSpmHost
        self.RemoteSpmPort = RemoteSpmPort
        self.RingTone = RingTone
        self.SbcName = SbcName
        self.ScreenSaver = ScreenSaver
        self.Secret = Secret
        self.Srtp = Srtp
        self.TimeFormat = TimeFormat
        self.TimeZone = TimeZone
        self.VlanInfos = VlanInfos
        self.XferType = XferType

from tcx_api.components.schemas.pbx.custom_queue_ringtone import CustomQueueRingtone
from tcx_api.components.schemas.pbx.phone_lldp_info import PhoneLldpInfo
from tcx_api.components.schemas.pbx.phone_device_vlan_info import PhoneDeviceVlanInfo

from tcx_api.components.schemas.pbx.enums import ProvType, XferTypeEnum
from typing import List

from tcx_api.util import Util


class PhoneSettings:
    def __init__(
        self,
        AllowCustomQueueRingtones: bool = None,
        Backlight: str = None,
        Codecs: list[str] = [],
        CustomLogo: str = None,
        CustomQueueRingtones: list[CustomQueueRingtone | dict] = [],
        DateFormat: str = None,
        Firmware: str = None,
        FirmwareLang: str = None,
        IsLogoCustomizable: bool = None,
        IsSBC: bool = None,
        LlDpInfo: PhoneLldpInfo | dict = None,
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
        VlanInfos: list[PhoneDeviceVlanInfo | dict] = [],
        XferType: XferTypeEnum | str = None,
    ) -> None:
        self.AllowCustomQueueRingtones = AllowCustomQueueRingtones
        self.Backlight = Backlight
        self.Codecs = Codecs
        self.CustomLogo = CustomLogo
        self.CustomQueueRingtones = Util.instanciate_list_of_objects(
            CustomQueueRingtones, CustomQueueRingtone
        )
        self.DateFormat = DateFormat
        self.Firmware = Firmware
        self.FirmwareLang = FirmwareLang
        self.IsLogoCustomizable = IsLogoCustomizable
        self.IsSBC = IsSBC
        self.LlDpInfo = Util.instanciate_object(LlDpInfo, PhoneLldpInfo)
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
        self.VlanInfos = Util.instanciate_list_of_objects(
            VlanInfos, PhoneDeviceVlanInfo
        )
        self.XferType = Util.inXferTypeEnum(XferType, XferTypeEnum)

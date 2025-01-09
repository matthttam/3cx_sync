import string
import random
from pydantic import TypeAdapter
import requests

from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import TcxStrEnum

from tcx_api.components.responses.other import HasDuplicatedEmailResponse
from tcx_api.components.schemas.pbx import Trunk
from tcx_api.components.parameters import (
    ExpandParameters,
    ListParameters,
    OrderbyParameters,
    SelectParameters,
)
from tcx_api.resources.trunks_exceptions import (
    TrunkCreateError,
    TrunkListError,
    TrunkGetError,
    TrunkUpdateError,
    TrunkDeleteError,
    TrunkHotdeskLogoutError,
)


class TrunkProperties(TcxStrEnum):
    AuthID = auto()
    AuthPassword = auto()
    ConfigurationIssue = auto()
    DidNumbers = auto()
    Direction = auto()
    DisableVideo = auto()
    E164CountryCode = auto()
    E164ProcessIncomingNumber = auto()
    EnableInboundCalls = auto()
    EnableOutboundCalls = auto()
    ExternalNumber: Optional[str] = None
    gateway: Optional[Gateway] = Field(None, alias="Gateway")
    Groups: list[UserGroup]
    Id: int
    InCIDFormatting: Optional[list[CIDFormatting]] = None
    IPRestriction: Optional[TypeOfIPDestriction] = None
    IsOnline: Optional[bool] = None
    IsWebmeetingBridge: Optional[bool] = None
    Messaging: Optional[TrunkMessaging] = None
    Number: Optional[str] = None
    OutboundCallerID: Optional[str] = None
    OutCIDFormatting: Optional[list[CIDFormatting]] = None
    PublicInfoGroups: Optional[list[str]] = None
    PublicIPinSIP: Optional[str] = None
    PublishInfo: Optional[bool] = None
    ReceiveExtensions: Optional[list[str]] = None
    ReceiveInfo: Optional[bool] = None
    RemoteMyPhoneUriHost: Optional[str] = None
    RemotePBXPreffix: Optional[str] = None
    RoutingRules: list[InboundRule]
    SecondaryRegistrar: Optional[str] = None
    SeparateAuthId: Optional[str] = None
    SimultaneousCalls: Optional[int] = None
    TransportRestriction: Optional[TypeOfTransportRestriction] = None
    TunnelEnabled: Optional[bool] = None
    TunnelRemoteAddr: Optional[str] = None
    TunnelRemotePort: Optional[int] = None
    UseSeparateAuthId: Optional[bool] = None


class ListTrunkParameters(
    ListParameters,
    OrderbyParameters,
    SelectParameters[TrunkProperties],
    ExpandParameters,
): ...


class GetTrunkParameters(SelectParameters[TrunkProperties], ExpandParameters): ...


class TrunksResource(APIResource):
    """Provides operations to manage the collection of Trunk entities."""

    endpoint: str = "Trunks"

    def get_endpoint(self, Trunk_id: int | None = None) -> str:
        """
        Returns the appropriate endpoint for Trunks or a specific Trunk.

        Args:
            Trunk_id (Optional[int]): The ID of the Trunk, if provided. If None, returns the endpoint for all Trunks.

        Returns:
            str: The formatted endpoint string.
        """
        if Trunk_id:
            return f"{self.endpoint}({Trunk_id})"
        return self.endpoint

    def create_Trunk(self, Trunk: dict):
        """
        Creates a new Trunk by sending a POST request to the Trunks endpoint.

        This method sends a dictionary representing the new Trunk to the API
        endpoint specified by `self.get_endpoint()`. If the API call fails
        with an HTTP error, a `TrunkCreateError` exception is raised.

        Args:
            Trunk (dict): A dictionary containing Trunk details to be created.
                        The dictionary should include all required fields
                        for Trunk creation as expected by the API.

        Raises:
            TrunkCreateError: If there is an issue creating the Trunk, such as
                            an HTTP error from the API.

        Example:
            Trunk_data = {
                "Id": 1234,
                "Name": "John Doe",
                "Email": "john.doe@example.com"
            }
            create_Trunk(Trunk_data)
        """

        try:
            self.api.post(self.get_endpoint(), Trunk)
        except requests.HTTPError as e:
            raise TrunkCreateError(e, Trunk)

    def list_Trunk(self, params: ListTrunkParameters) -> List[Trunk]:
        """
        Retrieves a list of Trunks by sending a GET request to the Trunks endpoint.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint()` with the provided parameters. The response is
        parsed and validated to return a list of `Trunk` objects. If the API
        call fails with an HTTP error, a `TrunkListError` exception is raised.

        Args:
            params (ListTrunkParameters): Parameters to filter or modify the
                                        Trunk list request. This should include
                                        query parameters expected by the API.

        Returns:
            List[Trunk]: A list of `Trunk` objects retrieved from the API response.

        Raises:
            TrunkListError: If there is an issue retrieving the list of Trunks,
                        such as an HTTP error from the API.

        Example:
            params = ListTrunkParameters(filter="status eq 'active'")
            Trunks = list_Trunk(params)
        """
        try:
            response = self.api.get(self.get_endpoint(), params)
            response_value = response.json().get("value")
            return TypeAdapter(List[Trunk]).validate_python(response_value)
        except requests.HTTPError as e:
            raise TrunkListError(e)

    def get_Trunk(self, Trunk_id: int, params: GetTrunkParameters) -> Trunk:
        """
        Retrieves a specific Trunk by sending a GET request to the Trunks endpoint with the given Trunk ID.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint(Trunk_id)` with the provided parameters. The response
        is parsed and validated to return a `Trunk` object. If the API call fails
        with an HTTP error, a `TrunkGetError` exception is raised.

        Args:
            Trunk_id (int): The unique identifier of the Trunk to retrieve.
            params (GetTrunkParameters): Parameters to filter or modify the
                                        Trunk retrieval request. This should include
                                        query parameters expected by the API.

        Returns:
            Trunk: The `Trunk` object retrieved from the API response.

        Raises:
            TrunkGetError: If there is an issue retrieving the Trunk, such as an HTTP
                        error from the API.

        Example:
            Trunk_id = 1234
            params = GetTrunkParameters()
            Trunk = get_Trunk(Trunk_id, params)
        """
        try:
            response = self.api.get(endpoint=self.get_endpoint(Trunk_id), params=params)
            return TypeAdapter(Trunk).validate_python(response.json())
        except requests.HTTPError as e:
            raise TrunkGetError(e, Trunk_id)

    def update_Trunk(self, Trunk: Trunk) -> None:
        """
        Updates an existing Trunk entity by sending a PATCH request to the Trunks endpoint.

        This method converts the given `Trunk` object to a dictionary, omitting unset
        and `None` values, and sends a PATCH request to the API endpoint with this data.
        If the API call fails with an HTTP error, a `TrunkUpdateError` exception is raised.

        Args:
            Trunk (Trunk): The `Trunk` object containing the updated information.
                        Only the fields that have been set (i.e., not `None` or
                        unset) will be included in the request.

        Raises:
            TrunkUpdateError: If there is an issue updating the Trunk, such as an HTTP
                            error from the API.

        Example:
            Trunk = Trunk(Id=1234, Name="Updated Name")
            update_Trunk(Trunk)
        """
        Trunk_id = self.get_Trunk_id(Trunk)
        try:
            Trunk_dict = Trunk.model_dump(
                exclude_unset=True,
                exclude_none=True,
                serialize_as_any=True,
                by_alias=True,
            )
            self.api.patch(endpoint=self.get_endpoint(Trunk_id), data=Trunk_dict)
        except requests.HTTPError as e:
            raise TrunkUpdateError(e, Trunk)

    def delete_Trunk(self, Trunk: Trunk | int) -> None:
        """
        Deletes a Trunk entity by sending a DELETE request to the Trunks endpoint.

        This method determines the Trunk ID from the provided `Trunk` object or ID, and
        sends a DELETE request to the API endpoint to remove the specified Trunk.
        If the API call fails with an HTTP error, a `TrunkDeleteError` exception is raised.

        Args:
            Trunk (Trunk | int): The `Trunk` object or Trunk ID representing the Trunk to be deleted.
                            If a `Trunk` object is provided, the method extracts the ID
                            from the object. If an integer is provided, it is used as the ID.

        Raises:
            TrunkDeleteError: If there is an issue deleting the Trunk, such as an HTTP error
                            from the API.

        Example:
            # Deleting a Trunk by passing a Trunk object
            Trunk = Trunk(Id=1234)
            delete_Trunk(Trunk)

            # Deleting a Trunk by passing the Trunk ID directly
            delete_Trunk(1234)
        """
        Trunk_id = self.get_Trunk_id(Trunk)
        try:
            self.api.delete(endpoint=self.get_endpoint(), params=Trunk_id)
        except requests.HTTPError as e:
            raise TrunkDeleteError(e, Trunk_id)

    def get_hotdesks_by_assigned_Trunk_number(
        self, Trunk_number: str
    ) -> List[Trunk] | None:
        """
        Retrieves the hotdesk assigned to a given Trunk based on their Trunk number.

        This method searches for a hotdesk associated with the specified Trunk number
        using the "HotdeskingAssignment" field. If a match is found, the first Trunk
        with the assigned hotdesk is returned. If no hotdesk is found, the function
        returns `None`.

        Args:
            Trunk_number (str): The Trunk number to search for a hotdesk assignment.

        Returns:
            Trunk | None: A `Trunk` object representing the hotdesk if found, or `None`
            if no hotdesk is assigned to the given Trunk number.

        Example:
            hotdesk_Trunk = get_hotdesk_by_assigned_Trunk_number("1234")
            if hotdesk_Trunk:
                print(f"Trunk is assigned to hotdesk {hotdesk_Trunk.Number}")
            else:
                print("No hotdesk assigned to this Trunk.")
        """
        params = ListTrunkParameters(filter=f"HotdeskingAssignment eq '{Trunk_number}'")
        Trunks = self.list_Trunk(params=params)
        if Trunks:
            return Trunks
        return None

    def clear_hotdesk_assignment(self, hotdesk_Trunk: Trunk | int):
        """
        Clear a hotdesk Trunk assignment.

        This method accepts either a `Trunk` object or a Trunk ID, identifies the Trunk,
        and sends a PATCH request to clear the hotdesking assignment for the specified Trunk.
        Once the request is processed, the hotdesk will no longer have any Trunk signed in to it.

        Args:
            Trunk (Trunk | int): The hotdesk Trunk to log any Trunk out of. Can be either a `Trunk` object or a Trunk ID.

        Raises:
            TrunkHotdeskLogoutError: If there is an error with the PATCH request.

        Example:
            # Using a hotdesk Trunk object
            hotdesk = get_hotdesk_by_assigned_Trunk_number(Trunk_number=1234)
            clear_hotdesk_assignment(hotdesk)

            # Using a hotdesk Trunk ID
            clear_hotdesk_assignment(34)
        """
        hotdesk_Trunk_id = self.get_Trunk_id(hotdesk_Trunk)
        try:
            self.api.patch(
                endpoint=self.get_endpoint(hotdesk_Trunk_id),
                data={"HotdeskingAssignment": ""},
            )
        except requests.HTTPError as e:
            TrunkHotdeskLogoutError(e, hotdesk_Trunk_id)

    def has_duplicate_email(self, Trunk: Trunk | int):
        return
        """ Not fully implemented yet """
        Trunk_id = self.get_Trunk_id(Trunk)
        try:
            response = self.api.get(
                f"{self.get_endpoint(Trunk_id)}/Pbx.HasDuplicatedEmail()"
            )
            HasDuplicatedEmailResponse(response)
        except requests.HTTPError as e:
            TrunkGetError(e, Trunk_id)

    def get_Trunk_id(self, Trunk: Trunk | int) -> int:
        """
        Helper method to extract the Trunk ID from either a Trunk object or an integer.

        Args:
            Trunk (Trunk | int): The Trunk object or Trunk ID.

        Returns:
            int: The Trunk ID.
        """
        if isinstance(Trunk, Trunk):
            return Trunk.Id
        return Trunk

    def get_new_Trunk(self):
        auth_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        # return json.loads('{"Require2FA": true, "SendEmailMissedCalls": true, "AuthID": "", "Phones": [], "Groups": [{"GroupId": 3078, "Rights": {"RoleName": "Trunks"}}], "CallUsEnableChat": true, "CallUsRequirement": "Both", "ClickToCallId": "testtest", "EmailAddress": "", "Mobile": "", "FirstName": "TEST", "LastName": "TEST", "Number": "10003", "OutboundCallerID": "", "PrimaryGroupId": 3078, "WebMeetingFriendlyName": "testtest", "WebMeetingApproveParticipants": false, "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>", "ForwardingProfiles": [], "MS365CalendarEnabled": true, "MS365ContactsEnabled": true, "MS365SignInEnabled": true, "MS365TeamsEnabled": true, "GoogleSignInEnabled": true, "Enabled": true, "Internal": false, "AllowOwnRecordings": false, "MyPhoneShowRecordings": false, "MyPhoneAllowDeleteRecordings": false, "MyPhoneHideForwardings": false, "RecordCalls": false, "HideInPhonebook": false, "PinProtected": false, "CallScreening": false, "AllowLanOnly": true, "SIPID": "", "EnableHotdesking": false, "PbxDeliversAudio": false, "SRTPMode": "SRTPDisabled", "Hours": {"Type": "OfficeHours"}, "OfficeHoursProps": [], "BreakTime": {"Type": "OfficeHours"}, "VMEnabled": true, "VMPIN": "923080", "VMEmailOptions": "Notification", "VMDisablePinAuth": false, "VMPlayCallerID": false, "VMPlayMsgDateTime": "None", "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB", "Greetings": [{"Type": "Default", "Filename": ""}]}')
        return {
            "Require2FA": True,
            "SendEmailMissedCalls": True,
            "AuthID": auth_id,
            "Phones": [],
            "Groups": [],
            "CallUsEnableChat": True,
            "CallUsRequirement": "Both",
            "ClickToCallId": "",
            "EmailAddress": "",
            "Mobile": "",
            "FirstName": "",
            "LastName": "",
            "Number": "",
            "OutboundCallerID": "",
            "PrimaryGroupId": 28,
            "WebMeetingFriendlyName": "",
            "WebMeetingApproveParticipants": False,
            "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>",
            "ForwardingProfiles": [],
            "MS365CalendarEnabled": True,
            "MS365ContactsEnabled": True,
            "MS365SignInEnabled": True,
            "MS365TeamsEnabled": True,
            "GoogleSignInEnabled": True,
            "Enabled": True,
            "Internal": False,
            "AllowOwnRecordings": False,
            "MyPhoneShowRecordings": False,
            "MyPhoneAllowDeleteRecordings": False,
            "MyPhoneHideForwardings": False,
            "RecordCalls": False,
            "HideInPhonebook": False,
            "PinProtected": False,
            "CallScreening": False,
            "AllowLanOnly": True,
            "SIPID": "",
            "EnableHotdesking": False,
            "PbxDeliversAudio": False,
            "SRTPMode": "SRTPDisabled",
            "Hours": {"Type": "OfficeHours"},
            "OfficeHoursProps": [],
            "BreakTime": {"Type": "OfficeHours"},
            "VMEnabled": True,
            "VMPIN": "",
            "VMEmailOptions": "Notification",
            "VMDisablePinAuth": False,
            "VMPlayCallerID": False,
            "VMPlayMsgDateTime": "None",
            "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB",
            "Greetings": [{"Type": "Default", "Filename": ""}],
        }

import string
import random
from pydantic import TypeAdapter
import requests

from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import TcxStrEnum

from tcx_api.components.responses.other import HasDuplicatedEmailResponse
from tcx_api.components.schemas.pbx import User
from tcx_api.components.parameters import (
    ExpandParameters,
    ListParameters,
    OrderbyParameters,
    SelectParameters,
)
from tcx_api.resources.users_exceptions import (
    UserCreateError,
    UserListError,
    UserGetError,
    UserUpdateError,
    UserDeleteError,
    UserHotdeskLogoutError,
)


class UserProperties(TcxStrEnum):
    AccessPassword = auto()
    AllowLanOnly = auto()
    AllowOwnRecordings = auto()
    AuthID = auto()
    AuthPassword = auto()
    Blfs = auto()
    BreakTime = auto()
    CallScreening = auto()
    CallUsEnableChat = auto()
    CallUsEnablePhone = auto()
    CallUsEnableVideo = auto()
    CallUsRequirement = auto()
    ClickToCallId = auto()
    ContactImage = auto()
    CurrentProfileName = auto()
    DeskphonePassword = auto()
    DisplayName = auto()
    EmailAddress = auto()
    Enable2FA = auto()
    Enabled = auto()
    EnableHotdesking = auto()
    FirstName = auto()
    ForwardingExceptions = auto()
    ForwardingProfiles = auto()
    GoogleSignInEnabled = auto()
    Greetings = auto()
    Groups = auto()
    HideInPhonebook = auto()
    HotdeskingAssignment = auto()
    Hours = auto()
    Id = auto()
    Internal = auto()
    IsRegistered = auto()
    Language = auto()
    LastName = auto()
    Mobile = auto()
    MS365CalendarEnabled = auto()
    MS365ContactsEnabled = auto()
    MS365SignInEnabled = auto()
    MS365TeamsEnabled = auto()
    MyPhoneAllowDeleteRecordings = auto()
    MyPhoneHideForwardings = auto()
    MyPhonePush = auto()
    MyPhoneShowRecordings = auto()
    Number = auto()
    OfficeHoursProps = auto()
    OutboundCallerID = auto()
    Phones = auto()
    PinProtected = auto()
    PinProtectTimeout = auto()
    PrimaryGroupId = auto()
    PromptSet = auto()
    ProvFile = auto()
    ProvLink = auto()
    RecordCalls = auto()
    RecordExternalCallsOnly = auto()
    Require2FA = auto()
    SendEmailMissedCalls = auto()
    SIPID = auto()
    Tags = auto()
    VMDisablePinAuth = auto()
    VMEmailOptions = auto()
    VMEnabled = auto()
    VMPIN = auto()
    VMPlayCallerID = auto()
    VMPlayMsgDateTime = auto()
    WebMeetingApproveParticipants = auto()
    WebMeetingFriendlyName = auto()


class ListUserParameters(
    ListParameters,
    OrderbyParameters,
    SelectParameters[UserProperties],
    ExpandParameters,
): ...


class GetUserParameters(SelectParameters[UserProperties], ExpandParameters): ...


class UsersResource(APIResource):
    """Provides operations to manage the collection of User entities."""

    endpoint: str = "Users"

    def get_endpoint(self, user_id: int | None = None) -> str:
        """
        Returns the appropriate endpoint for users or a specific user.

        Args:
            user_id (Optional[int]): The ID of the user, if provided. If None, returns the endpoint for all users.

        Returns:
            str: The formatted endpoint string.
        """
        if user_id:
            return f"{self.endpoint}({user_id})"
        return self.endpoint

    def create_user(self, user: dict):
        """
        Creates a new user by sending a POST request to the Users endpoint.

        This method sends a dictionary representing the new user to the API
        endpoint specified by `self.get_endpoint()`. If the API call fails
        with an HTTP error, a `UserCreateError` exception is raised.

        Args:
            user (dict): A dictionary containing user details to be created.
                        The dictionary should include all required fields
                        for user creation as expected by the API.

        Raises:
            UserCreateError: If there is an issue creating the user, such as
                            an HTTP error from the API.

        Example:
            user_data = {
                "Id": 1234,
                "Name": "John Doe",
                "Email": "john.doe@example.com"
            }
            create_user(user_data)
        """

        try:
            self.api.post(self.get_endpoint(), user)
        except requests.HTTPError as e:
            raise UserCreateError(e, user)

    def list_user(self, params: ListUserParameters) -> List[User]:
        """
        Retrieves a list of users by sending a GET request to the Users endpoint.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint()` with the provided parameters. The response is
        parsed and validated to return a list of `User` objects. If the API
        call fails with an HTTP error, a `UserListError` exception is raised.

        Args:
            params (ListUserParameters): Parameters to filter or modify the
                                        user list request. This should include
                                        query parameters expected by the API.

        Returns:
            List[User]: A list of `User` objects retrieved from the API response.

        Raises:
            UserListError: If there is an issue retrieving the list of users,
                        such as an HTTP error from the API.

        Example:
            params = ListUserParameters(filter="status eq 'active'")
            users = list_user(params)
        """
        try:
            response = self.api.get(self.get_endpoint(), params)
            response_value = response.json().get("value")
            return TypeAdapter(List[User]).validate_python(response_value)
        except requests.HTTPError as e:
            raise UserListError(e)

    def get_user(self, user_id: int, params: GetUserParameters) -> User:
        """
        Retrieves a specific user by sending a GET request to the Users endpoint with the given user ID.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint(user_id)` with the provided parameters. The response
        is parsed and validated to return a `User` object. If the API call fails
        with an HTTP error, a `UserGetError` exception is raised.

        Args:
            user_id (int): The unique identifier of the user to retrieve.
            params (GetUserParameters): Parameters to filter or modify the
                                        user retrieval request. This should include
                                        query parameters expected by the API.

        Returns:
            User: The `User` object retrieved from the API response.

        Raises:
            UserGetError: If there is an issue retrieving the user, such as an HTTP
                        error from the API.

        Example:
            user_id = 1234
            params = GetUserParameters()
            user = get_user(user_id, params)
        """
        try:
            response = self.api.get(endpoint=self.get_endpoint(user_id), params=params)
            return TypeAdapter(User).validate_python(response.json())
        except requests.HTTPError as e:
            raise UserGetError(e, user_id)

    def update_user(self, user: User) -> None:
        """
        Updates an existing user entity by sending a PATCH request to the Users endpoint.

        This method converts the given `User` object to a dictionary, omitting unset
        and `None` values, and sends a PATCH request to the API endpoint with this data.
        If the API call fails with an HTTP error, a `UserUpdateError` exception is raised.

        Args:
            user (User): The `User` object containing the updated information.
                        Only the fields that have been set (i.e., not `None` or
                        unset) will be included in the request.

        Raises:
            UserUpdateError: If there is an issue updating the user, such as an HTTP
                            error from the API.

        Example:
            user = User(Id=1234, Name="Updated Name")
            update_user(user)
        """
        user_id = self.get_user_id(user)
        try:
            user_dict = user.model_dump(
                exclude_unset=True,
                exclude_none=True,
                serialize_as_any=True,
                by_alias=True,
            )
            self.api.patch(endpoint=self.get_endpoint(user_id), data=user_dict)
        except requests.HTTPError as e:
            raise UserUpdateError(e, user)

    def delete_user(self, user: User | int) -> None:
        """
        Deletes a user entity by sending a DELETE request to the Users endpoint.

        This method determines the user ID from the provided `User` object or ID, and
        sends a DELETE request to the API endpoint to remove the specified user.
        If the API call fails with an HTTP error, a `UserDeleteError` exception is raised.

        Args:
            user (User | int): The `User` object or user ID representing the user to be deleted.
                            If a `User` object is provided, the method extracts the ID
                            from the object. If an integer is provided, it is used as the ID.

        Raises:
            UserDeleteError: If there is an issue deleting the user, such as an HTTP error
                            from the API.

        Example:
            # Deleting a user by passing a User object
            user = User(Id=1234)
            delete_user(user)

            # Deleting a user by passing the user ID directly
            delete_user(1234)
        """
        user_id = self.get_user_id(user)
        try:
            self.api.delete(endpoint=self.get_endpoint(), params=user_id)
        except requests.HTTPError as e:
            raise UserDeleteError(e, user_id)

    def get_hotdesks_by_assigned_user_number(
        self, user_number: str
    ) -> List[User] | None:
        """
        Retrieves the hotdesk assigned to a given user based on their user number.

        This method searches for a hotdesk associated with the specified user number
        using the "HotdeskingAssignment" field. If a match is found, the first user
        with the assigned hotdesk is returned. If no hotdesk is found, the function
        returns `None`.

        Args:
            user_number (str): The user number to search for a hotdesk assignment.

        Returns:
            User | None: A `User` object representing the hotdesk if found, or `None`
            if no hotdesk is assigned to the given user number.

        Example:
            hotdesk_user = get_hotdesk_by_assigned_user_number("1234")
            if hotdesk_user:
                print(f"User is assigned to hotdesk {hotdesk_user.Number}")
            else:
                print("No hotdesk assigned to this user.")
        """
        params = ListUserParameters(filter=f"HotdeskingAssignment eq '{user_number}'")
        users = self.list_user(params=params)
        if users:
            return users
        return None

    def clear_hotdesk_assignment(self, hotdesk_user: User | int):
        """
        Clear a hotdesk user assignment.

        This method accepts either a `User` object or a user ID, identifies the user,
        and sends a PATCH request to clear the hotdesking assignment for the specified user.
        Once the request is processed, the hotdesk will no longer have any user signed in to it.

        Args:
            user (User | int): The hotdesk user to log any user out of. Can be either a `User` object or a user ID.

        Raises:
            UserHotdeskLogoutError: If there is an error with the PATCH request.

        Example:
            # Using a hotdesk User object
            hotdesk = get_hotdesk_by_assigned_user_number(user_number=1234)
            clear_hotdesk_assignment(hotdesk)

            # Using a hotdesk user ID
            clear_hotdesk_assignment(34)
        """
        hotdesk_user_id = self.get_user_id(hotdesk_user)
        try:
            self.api.patch(
                endpoint=self.get_endpoint(hotdesk_user_id),
                data={"HotdeskingAssignment": ""},
            )
        except requests.HTTPError as e:
            UserHotdeskLogoutError(e, hotdesk_user_id)

    def has_duplicate_email(self, user: User | int):
        return
        """ Not fully implemented yet """
        user_id = self.get_user_id(user)
        try:
            response = self.api.get(
                f"{self.get_endpoint(user_id)}/Pbx.HasDuplicatedEmail()"
            )
            HasDuplicatedEmailResponse(response)
        except requests.HTTPError as e:
            UserGetError(e, user_id)

    def get_user_id(self, user: User | int) -> int:
        """
        Helper method to extract the user ID from either a User object or an integer.

        Args:
            user (User | int): The user object or user ID.

        Returns:
            int: The user ID.
        """
        if isinstance(user, User):
            return user.Id
        return user

    def get_new_user(self):
        auth_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        # return json.loads('{"Require2FA": true, "SendEmailMissedCalls": true, "AuthID": "", "Phones": [], "Groups": [{"GroupId": 3078, "Rights": {"RoleName": "users"}}], "CallUsEnableChat": true, "CallUsRequirement": "Both", "ClickToCallId": "testtest", "EmailAddress": "", "Mobile": "", "FirstName": "TEST", "LastName": "TEST", "Number": "10003", "OutboundCallerID": "", "PrimaryGroupId": 3078, "WebMeetingFriendlyName": "testtest", "WebMeetingApproveParticipants": false, "Blfs": "<PhoneDevice><BLFS/></PhoneDevice>", "ForwardingProfiles": [], "MS365CalendarEnabled": true, "MS365ContactsEnabled": true, "MS365SignInEnabled": true, "MS365TeamsEnabled": true, "GoogleSignInEnabled": true, "Enabled": true, "Internal": false, "AllowOwnRecordings": false, "MyPhoneShowRecordings": false, "MyPhoneAllowDeleteRecordings": false, "MyPhoneHideForwardings": false, "RecordCalls": false, "HideInPhonebook": false, "PinProtected": false, "CallScreening": false, "AllowLanOnly": true, "SIPID": "", "EnableHotdesking": false, "PbxDeliversAudio": false, "SRTPMode": "SRTPDisabled", "Hours": {"Type": "OfficeHours"}, "OfficeHoursProps": [], "BreakTime": {"Type": "OfficeHours"}, "VMEnabled": true, "VMPIN": "923080", "VMEmailOptions": "Notification", "VMDisablePinAuth": false, "VMPlayCallerID": false, "VMPlayMsgDateTime": "None", "PromptSet": "8210986B-9412-497f-AD77-3A554F4A9BDB", "Greetings": [{"Type": "Default", "Filename": ""}]}')
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

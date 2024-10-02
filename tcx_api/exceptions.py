import json
from requests import HTTPError
from tcx_api.components.schemas.ODataErrors import ErrorDetails, MainError, ODataError
from tcx_api.components.schemas.pbx import User


class APIError(Exception):
    """Base class for API-related errors."""

    def __init__(self, e: HTTPError, message: str = ""):
        super().__init__(message)
        self._http_error = e
        self.message = message
        self.api_error_message = ""
        self._parse_http_error()

    def _parse_http_error(self):
        """Parses the HTTPError and sets the api_error_message."""
        if not self._http_error.response:
            self.api_error_message = f"HTTP Error: {self._http_error}"
            return

        response_text = self._http_error.response.text
        if response_text:
            try:
                error_response = json.loads(response_text)
                odata_error = ODataError(**error_response)
                self.api_error_message = self._format_main_error(odata_error.error)
            except (json.JSONDecodeError, ValueError) as ex:
                self.api_error_message = f"Failed to parse error response: {ex}"
        else:
            self.api_error_message = f"HTTP Error: {self._http_error.response.reason}"

    def _format_main_error(self, main_error: MainError) -> str:
        """Formats the MainError into a readable string."""
        message = f"{f'[{main_error.code}] ' if main_error.code else ''}{main_error.message or 'Unknown error'}"
        if main_error.details:
            for detail in main_error.details:
                message += "\n" + self._format_error_details(detail)
        return message

    def _format_error_details(self, detail: ErrorDetails) -> str:
        """Formats individual error details into a readable string."""
        return f"[{detail.code}] {detail.message}{f' {detail.target}' if detail.target else ''}"

    def __str__(self) -> str:
        """Returns a string representation of the error."""
        return f"{self.message} {self.api_error_message}"


# class APIError(Exception):
#    """Base class for API-related errors."""
#
#    def __init__(self, e: HTTPError, message: str = ""):
#        self._http_error = e
#        self.message = message  # Set custom message if provided
#
#        if self._http_error.response.text:
#            self._parse_response_text(self._http_error.response.text)
#        else:
#            self.MainError = MainError(
#                code=str(self._http_error.response.status_code),
#                message=self._http_error.response.reason,
#            )
#            self.api_error_Message = str(self.MainError)
#
#    def _parse_response_text(self, response_text: str):
#        try:
#            self.response_error = json.loads(response_text)
#            error_content = self._get_error_content(self.response_error)
#            self.MainError = MainError(**error_content)
#            self.api_error_Message = self.format_main_error(self.MainError)
#        except (json.JSONDecodeError, KeyError) as ex:
#            self.api_error_Message = f"Failed to parse error response: {ex}"
#
#    def _get_error_content(self, response: dict) -> dict:
#        return response.get("error", {})
#
#    def format_main_error(self, error: MainError):
#        message = f"{f'[{error.code}] ' if error.code else ''}{error.message or 'Unknown error'}"
#
#        # Check if 'details' exists and is iterable
#        if hasattr(error, "details") and error.details:
#            for error_details in error.details:
#                message += "\n" + self.format_error_details(error_details)
#        return message
#
#    def format_error_details(self, error_details: ErrorDetails):
#        return f"[{error_details.code}] {error_details.message}{f' {error_details.target}' if error_details.target else ''}"
#
#    def __str__(self):
#        return f"{self.message} {self.api_error_Message}"


# class ListError(APIError):
#    """Error raised when there is an issue listing something."""
#
#    @property
#    def message(self):
#        return f"Unable to retrive {self.object}."
#
#
# class GetError(APIError):
#    """Error raised when there is an issue getting something."""
#
#    @property
#    def message(self):
#        return f"Unable to retrive {self.object}."
#
#
# class CreateError(APIError):
#    """Error raised when there is an issue creating something."""
#
#    @property
#    def message(self):
#        return f"Unable to create {self.object}."
#
#
# class UpdateError(APIError):
#    """Error raised when there is an issue updating something."""
#
#    @property
#    def message(self):
#        return f"Unable to update {self.object}."
#
#
# class GroupListError(ListError):
#    """Error raised when there is an issue listing groups."""
#
#    object = "groups"
#
#
# class GroupGetError(GetError):
#    """Error raised when there is an issue getting a user."""
#
#    object = "group"
#
#
# class GroupCreateError(CreateError):
#    """Error raised when there is an issue creating a user."""
#
#    object = "group"
#
#
# class GroupUpdateError(UpdateError):
#    """Error raised when there is an issue updating a user."""
#
#    object = "group"
#
#
# class UserListError(APIError):
#    """Error raised when there is an issue listing users."""
#
#    message = "Unable to retrieve users."
#
#
# class UserGetError(APIError):
#    """Error raised when there is an issue getting a user."""
#
#    message = "Unable to retrieve user."
#
#
# class UserCreateError(APIError):
#    """Error raised when there is an issue creating a user."""
#
#    message = "Unable to create user."
#
#
# class UserUpdateError(APIError):
#    """Error raised when there is an issue updating a user."""
#
#    message = "Unable to update user."


class APIAuthenticationError(Exception):
    """Exception raised when authentication fails

    Attributes:
        HTTP Response Error Message
        HTTP Response Code
    """

    def __init__(self, http_error: HTTPError):
        self.status_code = http_error.response.status_code
        self.error_message = str(http_error)

    def __str__(self):
        return f"Authentication Failure. {self.error_message} ({self.status_code})"

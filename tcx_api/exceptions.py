import json
from requests import HTTPError
from tcx_api.components.schemas.ODataErrors import ErrorDetails, MainError


class APIError(Exception):
    """Base class for API-related errors."""

    def __init__(self, e: HTTPError):
        self._http_error = e
        if self._http_error.response.text:
            self._parse_response_text(self._http_error.response.text)
        else:
            self.MainError = MainError(
                code=str(self._http_error.response.status_code), message=self._http_error.response.reason)
            self.api_error_Message = str(self.MainError)

    def _parse_response_text(self, response_text: str):
        self.response_error = json.loads(response_text)
        self.MainError = MainError(**self.response_error['error'])
        self.api_error_Message = self.format_main_error(self.MainError)

    def format_main_error(self, error: MainError):
        message = f"{f'[{error.code}] 'if error.code else ''}{
            error.message}"
        for error_details in error.details:
            message += '\n' + self.format_error_details(error_details)
        return message

    def format_error_details(self, error_details: ErrorDetails):
        # code = error_details.code
        # message = error_details.message
        # message_info = message.split('.')
        return f"[{error_details.code}] {error_details.message}{f' {error_details.target}' if error_details.target else ''}"

    def __str__(self):
        return f"{getattr(self, 'message', '')} " + self.api_error_Message
        # return self.message or ""


class UserListError(APIError):
    """Error raised when there is an issue listing users."""
    message = "Unable to retrieve users."


class UserGetError(APIError):
    """Error raised when there is an issue getting a user."""
    message = "Unable to retrieve user."


class UserCreateError(APIError):
    """Error raised when there is an issue creating a user."""
    message = "Unable to create user."


class UserUpdateError(APIError):
    """Error raised when there is an issue updating a user."""
    message = "Unable to update user."


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

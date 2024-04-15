class APIError(Exception):
    """Base class for API-related errors."""


class UserListError(APIError):
    """Error raised when there is an issue listing users."""


class UserGetError(APIError):
    """Error raised when there is an issue getting a use."""


class APIAuthenticationError(Exception):
    """Exception raised when authentication fails

    Attributes:
        HTTP Response Error Message
        HTTP Response Code
    """

    def __init__(self, http_response_status_code, http_response_error_message):
        self.message = f"Authentication Failure. {http_response_error_message} ({http_response_status_code})"
        super().__init__(self.message)

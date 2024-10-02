from tcx_api.exceptions import APIError
from requests import HTTPError
from tcx_api.components.schemas.pbx import User


class UserCreateError(APIError):
    """Error raised when there is an issue creating a user."""

    def __init__(self, e: HTTPError, user: dict):
        user_number = getattr(user, "Number", "N/A")
        error_message = f"Unable to create user with number {user_number}."
        super().__init__(e, error_message)


class UserListError(APIError):
    """Error raised when there is an issue listing users."""

    def __init__(self, e: HTTPError):
        super().__init__(e, "Unable to retrieve users.")


class UserGetError(APIError):
    """Error raised when there is an issue getting a user."""

    def __init__(self, e: HTTPError, user_id: int):
        error_message = f"Unable to retrieve user with ID {user_id}."
        super().__init__(e, error_message)


class UserUpdateError(APIError):
    """Error raised when there is an issue updating a user."""

    def __init__(self, e: HTTPError, user: User):
        user_id = user.Id
        user_number = getattr(user, "Number", "N/A")
        error_message = (
            f"Unable to update user with ID {user_id} and number {user_number}."
        )
        super().__init__(e, error_message)


class UserDeleteError(APIError):
    """Error raised when there is an issue deleting a user."""

    def __init__(self, e: HTTPError, user_id: int):
        error_message = f"Unable to delete user with ID {user_id}."
        super().__init__(e, error_message)


class UserHotdeskLogoutError(APIError):
    """Error raised when there is an issue signing a user out of a hotdesk."""

    def __init__(self, e: HTTPError, hotdesk_user_id: int):
        error_message = f"Unable to clear hotdesking assignment of hotdesk with ID {hotdesk_user_id} out of assigned hotdesk."
        super().__init__(e, error_message)

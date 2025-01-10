from tcx_api.exceptions import APIError
from requests import HTTPError
from tcx_api.components.schemas.pbx import Trunk


class TrunkCreateError(APIError):
    """Error raised when there is an issue creating a trunk."""

    def __init__(self, e: HTTPError, trunk: dict):
        trunk_number = getattr(trunk, "Number", "N/A")
        error_message = f"Unable to create trunk with number {trunk_number}."
        super().__init__(e, error_message)


class TrunkListError(APIError):
    """Error raised when there is an issue listing trunks."""

    def __init__(self, e: HTTPError):
        super().__init__(e, "Unable to retrieve trunks.")


class TrunkGetError(APIError):
    """Error raised when there is an issue getting a trunk."""

    def __init__(self, e: HTTPError, trunk_id: int):
        error_message = f"Unable to retrieve trunk with ID {trunk_id}."
        super().__init__(e, error_message)


class TrunkUpdateError(APIError):
    """Error raised when there is an issue updating a trunk."""

    def __init__(self, e: HTTPError, trunk: Trunk):
        trunk_id = trunk.Id
        trunk_number = getattr(trunk, "Number", "N/A")
        error_message = (
            f"Unable to update trunk with ID {trunk_id} and number {trunk_number}."
        )
        super().__init__(e, error_message)


class TrunkDeleteError(APIError):
    """Error raised when there is an issue deleting a trunk."""

    def __init__(self, e: HTTPError, trunk_id: int):
        error_message = f"Unable to delete trunk with ID {trunk_id}."
        super().__init__(e, error_message)


class TrunkGetByNumberError(APIError):
    """Error raised when there is an issue getting a trunk by number."""

    def __init__(self, e: HTTPError, number: str):
        error_message = f"Unable to retrieve trunk with number '{number}'."
        super().__init__(e, error_message)


class TrunkGetInitTrunkError(APIError):
    """Error raised when there is an issue initializing a new trunk with a template."""

    def __init__(self, e: HTTPError, template: str):
        error_message = f"Unable to create trunk with template '{template}'."
        super().__init__(e, error_message)
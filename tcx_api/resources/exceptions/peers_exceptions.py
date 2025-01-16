from tcx_api.exceptions import APIError
from requests import HTTPError
from tcx_api.components.schemas.pbx import Peer


class PeerCreateError(APIError):
    """Error raised when there is an issue creating a peer."""

    def __init__(self, e: HTTPError, peer: dict):
        peer_number = getattr(peer, "Number", "N/A")
        error_message = f"Unable to create peer with number {peer_number}."
        super().__init__(e, error_message)


class PeerListError(APIError):
    """Error raised when there is an issue listing peers."""

    def __init__(self, e: HTTPError):
        super().__init__(e, "Unable to retrieve peers.")


class PeerGetError(APIError):
    """Error raised when there is an issue getting a peer."""

    def __init__(self, e: HTTPError, peer_id: int):
        error_message = f"Unable to retrieve peer with ID {peer_id}."
        super().__init__(e, error_message)


class PeerUpdateError(APIError):
    """Error raised when there is an issue updating a peer."""

    def __init__(self, e: HTTPError, peer: Peer):
        peer_id = peer.Id
        peer_number = getattr(peer, "Number", "N/A")
        error_message = (
            f"Unable to update peer with ID {peer_id} and number {peer_number}."
        )
        super().__init__(e, error_message)


class PeerDeleteError(APIError):
    """Error raised when there is an issue deleting a peer."""

    def __init__(self, e: HTTPError, peer_id: int):
        error_message = f"Unable to delete peer with ID {peer_id}."
        super().__init__(e, error_message)


class PeerGetByNumberError(APIError):
    """Error raised when there is an issue getting a peer by number."""

    def __init__(self, e: HTTPError, user_number: int):
        error_message = f"Unable to get peer with number {user_number}."
        super().__init__(e, error_message)

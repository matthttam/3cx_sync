import string
import random
from pydantic import TypeAdapter
import requests

from typing import List
from enum import auto
from tcx_api.resources.api_resource import APIResource
from tcx_api.util import create_enum_from_model

from tcx_api.components.responses.other import HasDuplicatedEmailResponse
from tcx_api.components.schemas.pbx import Trunk
from tcx_api.components.parameters import (
    ExpandParameters,
    ListParameters,
    OrderbyParameters,
    SelectParameters,
)
from tcx_api.resources.exceptions.trunks_exceptions import (
    TrunkCreateError,
    TrunkListError,
    TrunkGetError,
    TrunkUpdateError,
    TrunkDeleteError,
    TrunkGetByNumberError,
    TrunkGetInitTrunkError,
)

TrunkProperties = create_enum_from_model(Trunk)

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

    def create_trunk(self, trunk: dict):
        """
        Creates a new trunk by sending a POST request to the Trunks endpoint.

        This method sends a dictionary representing the new trunk to the API
        endpoint specified by `self.get_endpoint()`. If the API call fails
        with an HTTP error, a `TrunkCreateError` exception is raised.

        Args:
            trunk (dict): A dictionary containing trunk details to be created.
                        The dictionary should include all required fields
                        for trunk creation as expected by the API.

        Raises:
            TrunkCreateError: If there is an issue creating the trunk, such as
                            an HTTP error from the API.

        Example:
            trunk_data = {
                "Id": 1234,
                "Name": "John Doe",
                "Email": "john.doe@example.com"
            }
            create_trunk(trunk_data)
        """

        try:
            self.api.post(self.get_endpoint(), trunk)
        except requests.HTTPError as e:
            raise TrunkCreateError(e, trunk)

    def list_trunk(self, params: ListTrunkParameters) -> List[Trunk]:
        """
        Retrieves a list of trunks by sending a GET request to the Trunks endpoint.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint()` with the provided parameters. The response is
        parsed and validated to return a list of `Trunk` objects. If the API
        call fails with an HTTP error, a `TrunkListError` exception is raised.

        Args:
            params (ListTrunkParameters): Parameters to filter or modify the
                                        trunk list request. This should include
                                        query parameters expected by the API.

        Returns:
            List[Trunk]: A list of `Trunk` objects retrieved from the API response.

        Raises:
            TrunkListError: If there is an issue retrieving the list of trunks,
                        such as an HTTP error from the API.

        Example:
            params = ListTrunkParameters(filter="status eq 'active'")
            trunks = list_trunk(params)
        """
        try:
            response = self.api.get(self.get_endpoint(), params)
            response_value = response.json().get("value")
            return TypeAdapter(List[Trunk]).validate_python(response_value)
        except requests.HTTPError as e:
            raise TrunkListError(e)

    def get_trunk(self, trunk_id: int, params: GetTrunkParameters) -> Trunk:
        """
        Retrieves a specific trunk by sending a GET request to the Trunks endpoint with the given trunk ID.

        This method sends a GET request to the API endpoint specified by
        `self.get_endpoint(trunk_id)` with the provided parameters. The response
        is parsed and validated to return a `Trunk` object. If the API call fails
        with an HTTP error, a `TrunkGetError` exception is raised.

        Args:
            trunk_id (int): The unique identifier of the trunk to retrieve.
            params (GetTrunkParameters): Parameters to filter or modify the
                                        trunk retrieval request. This should include
                                        query parameters expected by the API.

        Returns:
            Trunk: The `Trunk` object retrieved from the API response.

        Raises:
            TrunkGetError: If there is an issue retrieving the trunk, such as an HTTP
                        error from the API.

        Example:
            trunk_id = 1234
            params = GetTrunkParameters()
            trunk = get_trunk(trunk_id, params)
        """
        try:
            response = self.api.get(endpoint=self.get_endpoint(trunk_id), params=params)
            return TypeAdapter(Trunk).validate_python(response.json())
        except requests.HTTPError as e:
            raise TrunkGetError(e, trunk_id)

    def update_trunk(self, trunk: Trunk) -> None:
        """
        Updates an existing trunk entity by sending a PATCH request to the Trunks endpoint.

        This method converts the given `Trunk` object to a dictionary, omitting unset
        and `None` values, and sends a PATCH request to the API endpoint with this data.
        If the API call fails with an HTTP error, a `TrunkUpdateError` exception is raised.

        Args:
            trunk (Trunk): The `Trunk` object containing the updated information.
                        Only the fields that have been set (i.e., not `None` or
                        unset) will be included in the request.

        Raises:
            TrunkUpdateError: If there is an issue updating the trunk, such as an HTTP
                            error from the API.

        Example:
            trunk = Trunk(Id=1234, Name="Updated Name")
            update_trunk(trunk)
        """
        trunk_id = self.get_trunk_id(trunk)
        try:
            trunk_dict = trunk.model_dump(
                exclude_unset=True,
                exclude_none=True,
                serialize_as_any=True,
                by_alias=True,
            )
            self.api.patch(endpoint=self.get_endpoint(trunk_id), data=trunk_dict)
        except requests.HTTPError as e:
            raise TrunkUpdateError(e, trunk)

    def delete_trunk(self, trunk: Trunk | int) -> None:
        """
        Deletes a trunk entity by sending a DELETE request to the Trunks endpoint.

        This method determines the trunk ID from the provided `Trunk` object or ID, and
        sends a DELETE request to the API endpoint to remove the specified trunk.
        If the API call fails with an HTTP error, a `TrunkDeleteError` exception is raised.

        Args:
            trunk (Trunk | int): The `Trunk` object or trunk ID representing the trunk to be deleted.
                            If a `Trunk` object is provided, the method extracts the ID
                            from the object. If an integer is provided, it is used as the ID.

        Raises:
            TrunkDeleteError: If there is an issue deleting the trunk, such as an HTTP error
                            from the API.

        Example:
            # Deleting a trunk by passing a Trunk object
            trunk = Trunk(Id=1234)
            delete_trunk(trunk)

            # Deleting a trunk by passing the trunk ID directly
            delete_trunk(1234)
        """
        trunk_id = self.get_trunk_id(trunk)
        try:
            self.api.delete(endpoint=self.get_endpoint(), params=trunk_id)
        except requests.HTTPError as e:
            raise TrunkDeleteError(e, trunk_id)

    def get_trunk_id(self, trunk: Trunk | int) -> int:
        """
        Helper method to extract the trunk ID from either a Trunk object or an integer.

        Args:
            trunk (Trunk | int): The trunk object or trunk ID.

        Returns:
            int: The trunk ID.
        """
        if isinstance(trunk, Trunk):
            return trunk.Id
        return trunk

    def get_trunk_by_number(self, number: str):
        """
        Provides operations to manage the collection of Trunk entities.

        Args:
            number:
        """
        try:
            
            response = self.api.get(
                endpoint=self.get_endpoint(action=f"Pbx.GetTrunkByNumber(number='{number}')")
            )
            return TypeAdapter(Trunk).validate_python(response.json())
        except requests.HTTPError as e:
            raise TrunkGetByNumberError(e, number)

    def get_new_trunk(self, template='Callcentric.pv.xml'):
        try:
            response = self.api.get(
                endpoint=self.get_endpoint(action=f"Pbx.InitTrunk(template='{template}')")
            )
            return TypeAdapter(Trunk).validate_python(response.json())
        except requests.HTTPError as e:
            raise TrunkGetInitTrunkError(e, template)
from pydantic import conlist
from tcx_api.components.response import Response


class ODataCountResponse:
    type: int
    format: int


class StringCollectionResponse(Response):
    value: conlist(str)


class Is2FAEnabledResponse(Response):
    pass


class HasDuplicatedEmailResponse(Response):
    pass


class GetRestrictionsResponse(Response):
    pass


class GetMyGroupPartnerInfoResponse(Response):
    pass

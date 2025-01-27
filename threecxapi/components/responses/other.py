from threecxapi.components.response import Response


class ODataCountResponse:
    type: int
    format: int


class StringCollectionResponse(Response):
    value: list[str]


class Is2FAEnabledResponse(Response):
    pass


class HasDuplicatedEmailResponse(Response):
    value: bool = False


class GetRestrictionsResponse(Response):
    pass


class GetMyGroupPartnerInfoResponse(Response):
    pass

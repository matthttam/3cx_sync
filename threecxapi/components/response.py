from pydantic import BaseModel, Field


class Response(BaseModel):
    context: str = Field(None, alias="@odata.context")
    count: int = Field(None, alias="@odata.count")

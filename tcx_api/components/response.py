from pydantic import BaseModel, Field


class Response(BaseModel):
    context: str = Field(None, alias="@odata.context")
    # '@odata.count': int

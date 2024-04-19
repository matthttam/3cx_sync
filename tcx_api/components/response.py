from pydantic import BaseModel


class Response(BaseModel):
    # '@odata.context': str
    # '@odata.count': int
    context: str
    count: int

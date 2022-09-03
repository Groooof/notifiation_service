import pydantic as pd


class RequestMessage(pd.BaseModel):
    id: int
    phone: str
    text: str


class Response(pd.BaseModel):
    code: int
    message: str

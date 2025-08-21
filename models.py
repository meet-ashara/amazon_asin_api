from pydantic import BaseModel

class AsinRequest(BaseModel):
    asin: str

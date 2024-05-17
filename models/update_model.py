from pydantic import BaseModel
from typing import List, Any

class UpdateRequest(BaseModel):
    memberId: int
    newHashtag: List[str]

class UpdateResponse(BaseModel):
    message: str
    updated_data: List[Any]

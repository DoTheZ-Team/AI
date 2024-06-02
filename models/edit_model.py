from pydantic import BaseModel
from typing import List, Any

class EditRequest(BaseModel):
    blogId: int
    changedHashtag: List[str]

class EditResponse(BaseModel):
    message: str
    changedHashtag: EditRequest

from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    member_id: int
    content: str
    score: float

class Recommendations(BaseModel):
    recommendations: List[Recommendation]
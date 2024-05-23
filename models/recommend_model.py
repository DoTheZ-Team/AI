from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    memberId: int
    followIds: List[int]

class Recommendations(BaseModel):
    recommendMemberId: List[int]

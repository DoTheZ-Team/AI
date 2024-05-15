# models/request_models.py
from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    memberId: int
    followsId: List[int]

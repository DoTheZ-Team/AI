from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    blogId: int
    followIds: List[int]

class Recommendations(BaseModel):
    recommendBlogId: List[int]

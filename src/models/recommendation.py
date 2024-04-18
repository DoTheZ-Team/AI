from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    member_id: int
    content: str
    score: float
    
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "content": self.content,
            "score": self.score
        }

class Recommendations(BaseModel):
    recommendations: List[Recommendation]
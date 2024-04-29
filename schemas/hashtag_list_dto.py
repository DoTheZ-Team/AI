from pydantic import BaseModel
from typing import List
from schemas.HashtagDTO import Hashtag

class HashtagList(BaseModel):
    member_id: int
    hashtags: List[Hashtag]
    
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "hashtags": [hashtag.hashtag for hashtag in self.hashtags]
        }

from datetime import datetime
from pydantic import BaseModel

class Hashtag(BaseModel):
    member_id: int
    post_id: int
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def to_dict(self):
        return {
            "post_id": self.post_id,
            "member_id": self.member_id,
            "content": self.content
        }

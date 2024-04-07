from datetime import datetime
from odmantic import Model

# 해새태그 모델
class Hashtag(Model):
    # primary key 설정 아직 안해둠
    member_id: int
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

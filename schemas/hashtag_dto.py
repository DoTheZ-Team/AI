from pydantic import BaseModel

class Hashtag(BaseModel):
    hashtag: str
    
    def to_dict(self):
        return {
            "hashtag": self.hashtag
        }
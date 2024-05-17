from fastapi import APIRouter
from models.update_model import UpdateRequest, UpdateResponse
from db.database import es_client
import services.update_serivce as updatesvs

updates_router = APIRouter()

# update 로직
@updates_router.post("/update")
async def update_user(request: UpdateRequest):
    # newHashtag 리스트를 문자열로 결합
    new_hashtag = " ".join(request.newHashtag)
    
    # data, vectorizer = await updatesvs.update(request.memberId, new_content, es_client)
    data = await updatesvs.update(request.memberId, new_hashtag, es_client)
    
    return UpdateResponse(message="User data updated successfully", updated_data=data)
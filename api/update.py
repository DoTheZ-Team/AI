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
    
    data = await updatesvs.update(request.memberId, new_hashtag, es_client)
    
    # numpy.int64 타입을 int로 변환
    for item in data:
        item['member_id'] = int(item['member_id'])
    
    return UpdateResponse(message="해시태그 업로드가 완료되었습니다.", updated_data=data)
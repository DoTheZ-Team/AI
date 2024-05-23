from fastapi import APIRouter, Body
from models.update_model import UpdateRequest, UpdateResponse
from db.database import es_client
import services.update_serivce as updatesvs

updates_router = APIRouter()

@updates_router.post("/hashtags", response_model=UpdateResponse, summary="해시태그 추가", description="사용자의 해시태그에 새로 해시태그를 추가하는 API입니다.\n 블로그 서비스와 통신을 진행할 API입니다.")
async def update_blog(request: UpdateRequest  = Body(..., example={
        "blogId": "1",
        "followIds": ["2", "3"]
    })):
    
    # newHashtag 리스트를 문자열로 결합
    new_hashtag = " ".join(request.newHashtag)
    
    data = await updatesvs.update(request.blogId, new_hashtag, es_client)
    
    # numpy.int64 타입을 int로 변환
    for item in data:
        item['blog_id'] = int(item['blog_id'])
    
    return UpdateResponse(message="해시태그 업로드가 완료되었습니다.", updated_data=data)
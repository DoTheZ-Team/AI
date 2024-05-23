from fastapi import APIRouter
from models.update_model import UpdateRequest, UpdateResponse
from db.database import es_client
import services.update_serivce as updatesvs

updates_router = APIRouter()

@updates_router.post("/update", response_model=UpdateResponse, summary="해시태그 추가", description="사용자의 해시태그에 새로 해시태그를 추가하는 API입니다.\n 블로그 서비스와 통신을 진행할 API입니다.")
async def update_user(request: UpdateRequest):
    """
    유저 id값을 기반으로 새로 추가된 해시태그를 데이터베이스에 업데이트 하는 API입니다.
    블로그 서비스와 통신을 진행할 API입니다.

    - **memberId**: 추천을 요청하는 사용자의 ID
    - **changedHashtag**: 새로 추가된 해시태그
    """
    
    # newHashtag 리스트를 문자열로 결합
    new_hashtag = " ".join(request.newHashtag)
    
    data = await updatesvs.update(request.memberId, new_hashtag, es_client)
    
    # numpy.int64 타입을 int로 변환
    for item in data:
        item['member_id'] = int(item['member_id'])
    
    return UpdateResponse(message="해시태그 업로드가 완료되었습니다.", updated_data=data)
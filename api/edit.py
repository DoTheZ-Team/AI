from fastapi import APIRouter
from models.edit_model import EditRequest, EditResponse
from db.database import es_client
import services.edit_service as editsvs

edits_router = APIRouter()

# 해시태그 수정 및 삭제로직
# 수정 또는 삭제 시 남아있는 모든 해시태그 값을 받고 새로 업데이트를 진행
@edits_router.post("/edit", response_model=EditResponse, summary="해시태그 일부 삭제 또는 전체 삭제", description="사용자의 해시태그를 전부 삭제 또는 일부를 삭제하는 API입니다.\n 블로그 서비스와 통신을 진행할 API입니다.")
async def update_user(request: EditRequest):
    """
    유저 id값을 기반으로 삭제된 해시태그를 데이터베이스에 업데이트 하는 API입니다.
    블로그 서비스와 통신을 진행할 API입니다.

    - **memberId**: 추천을 요청하는 사용자의 ID
    - **changedHashtag**: 일부 삭제 또는 전체 삭제 후의 해시태그 결과 리스트(새로 저장할 해시태그)
    """

    data = await editsvs.edit(request.memberId, request.changedHashtag, es_client)
    
    return EditResponse(
        message="해시태그 수정이 완료되었습니다.", changedHashtag=request)

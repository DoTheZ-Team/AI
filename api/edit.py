from fastapi import APIRouter
from models.edit_model import EditRequest, EditResponse
from db.database import es_client
import services.edit_service as editsvs

edits_router = APIRouter()

# 해시태그 수정 및 삭제로직
# 수정 또는 삭제 시 남아있는 모든 해시태그 값을 받고 새로 업데이트를 진행
@edits_router.post("/edit")
async def update_user(request: EditRequest):
    data = await editsvs.edit(request.memberId, request.changedHashtag, es_client)
    
    return EditResponse(
        message="해시태그 수정이 완료되었습니다.", changedHashtag=request)

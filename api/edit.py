from fastapi import APIRouter, Body
from models.edit_model import EditRequest, EditResponse
from db.database import es_client
import services.edit_service as editsvs

edits_router = APIRouter()

# 해시태그 수정 및 삭제로직
# 수정 또는 삭제 시 남아있는 모든 해시태그 값을 받고 새로 업데이트를 진행
@edits_router.post("/editings", response_model=EditResponse, summary="해시태그 일부 삭제 또는 전체 삭제", description="블로그에 저장된 해시태그를 전부 삭제 또는 일부를 삭제하는 API입니다.\n 블로그 서비스와 통신을 진행할 API입니다.")
async def update_blog(request: EditRequest = Body(..., example={
        "blogId": "1",
        "changedHashtag": ["exampleTag1", "exampleTag2"]
    })):

    data = await editsvs.edit(request.blogId, request.changedHashtag, es_client)
    
    return EditResponse(
        message="해시태그 수정이 완료되었습니다.", changedHashtag=request)

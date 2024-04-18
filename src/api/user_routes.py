from fastapi import APIRouter, Form
import src.services.hashtag_service as svs
from src.database import es_client

router = APIRouter()

# @router.post("/user/hashtag/update")
# async def update_hashtag(member_id: int = Form(), content: str = Form()):
#     hashtag = await controller.update_hashtag(member_id, content)
#     return hashtag

@router.get("/user/{member_id}/recommend")
async def recommend_user(member_id: int):
    # if(새로운 해시태그 추가): 아래의 함수 실행: 새로운 해시태그 추가 부분을 어떻게 진행해야 될지 몰라서 일단 보류
    # svs.update_hashtag(member_id, new_hashtag, res)
    # tf-idf 수행
    tfidf_matrix, data = svs.TF_IDF()
    es_client = svs.index_creation(tfidf_matrix)
    docs = svs.prepare_documents(tfidf_matrix)
    svs.indexing(docs, es_client)
   
    # if(해시태그가 기존 그대로임): TF-IDF 수행 안하고 바로 아래 함수부터 실행
    res = svs.find_hashtags(member_id)
    await svs.recommend_user(member_id, es_client)

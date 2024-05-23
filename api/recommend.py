from fastapi import APIRouter
from models.recommend_model import Recommendations, RecommendationRequest
from db.database import es_client
import services.recommend_service as recommendsvs
import services.tmp.tf_idf_service as tfidfsvs

recommends_router = APIRouter()

# 추천 결과 반환 API
@recommends_router.get("/recommend", response_model=Recommendations, summary="유저 추천", description="유저 id값과 팔로우된 사람들의 정보를 바탕으로 유저 추천을 해주는 API입니다. \n 블로그 서비스와 통신을 진행할 API입니다.")
async def recommend_user(request: RecommendationRequest):
    # # 혹시나 인덱스 삭제 후 생성할 때 사용하기 위해 둔 부분
    # tfidf_matrix, vectorizer = tfidfsvs.TF_IDF()
    # es_client = await tfidfsvs.index_creation(tfidf_matrix)
    # docs = tfidfsvs.prepare_documents(tfidf_matrix)
    # await tfidfsvs.indexing(docs, es_client)
    # return
    
    """
    유저 id값과 팔로우된 사람들의 정보를 바탕으로 유저 추천을 해주는 API입니다.
    블로그 서비스와 통신을 진행할 API입니다.

    - **memberId**: 추천을 요청하는 사용자의 ID
    - **followIds**: 팔로우하는 사용자의 ID 목록
    """

    response = await recommendsvs.recommend(request.memberId, request.followIds, es_client)
    
    recommend_member_ids = [hit['_source']['member_id'] for hit in response['hits']['hits']]
    
    return Recommendations(recommendMemberId=recommend_member_ids)
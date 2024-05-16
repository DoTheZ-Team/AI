from fastapi import APIRouter
from models.recommend_model import Recommendation, Recommendations, RecommendationRequest
from db.database import es_client
import services.recommend_service as recommendsvs
import services.tmp.tf_idf_service as tfidfsvs

recommends_router = APIRouter()

# 추천 결과 반환 API
@recommends_router.post("/recommend", response_model=Recommendations)
async def recommend_user(request: RecommendationRequest):
    # # 혹시나 인덱스 삭제 후 생성할 때 사용하기 위해 둔 부분
    # tfidf_matrix, vectorizer = tfidfsvs.TF_IDF()
    # es_client = await tfidfsvs.index_creation(tfidf_matrix)
    # docs = tfidfsvs.prepare_documents(tfidf_matrix)
    # await tfidfsvs.indexing(docs, es_client)
    # return

    response = await recommendsvs.recommend(request.memberId, request.followsId, es_client)
    
    results = [Recommendation(
        member_id=hit['_source']['member_id'],
        content=hit['_source']['content'],
        score=hit['_score']
    ) for hit in response['hits']['hits']]
    
    return Recommendations(recommendations=results)
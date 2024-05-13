from fastapi import APIRouter
from models.recommendation import Recommendation, Recommendations
from db.database import es_client
import services.recommend_service as recommendsvs

router = APIRouter()

# 추천 결과 반환 API
@router.get("/user/{member_id}/recommend", response_model=Recommendations)
async def recommend_user(member_id: int):

    response = await recommendsvs.recommend(member_id, es_client)
    
    results = [Recommendation(
        member_id=hit['_source']['member_id'],
        content=hit['_source']['content'],
        score=hit['_score']
    ) for hit in response['hits']['hits']]
    return Recommendations(recommendations=results)

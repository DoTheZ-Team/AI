from fastapi import APIRouter
from models.recommendation_response import Recommendation, Recommendations
from models.recommend_request import RecommendationRequest
from db.database import es_client
import services.recommend_service as recommendsvs

router = APIRouter()

# 추천 결과 반환 API
@router.post("/recommends", response_model=Recommendations)
async def recommend_user(request: RecommendationRequest):

    response = await recommendsvs.recommend(request.memberId, request.followsId, es_client)
    
    results = [Recommendation(
        member_id=hit['_source']['member_id'],
        content=hit['_source']['content'],
        score=hit['_score']
    ) for hit in response['hits']['hits']]
    
    return Recommendations(recommendations=results)
from fastapi import APIRouter, Form, HTTPException
import services.hashtag_service as svs
from db.database import es_client
from models.recommendation import Recommendation, Recommendations

router = APIRouter()

# 추천 결과 반환 API
@router.get("/user/{member_id}/recommend", response_model=Recommendations)
async def recommend_user(member_id: int):
    # if(해시태그가 기존 그대로임): TF-IDF 수행 안하고 바로 아래 함수부터 실행
    # res = svs.find_hashtags(member_id)
    response = await svs.recommend_user(member_id, es_client)
    
    try:
        if response['hits']['hits']:
            results = [Recommendation(
                member_id=hit['_source']['member_id'],
                content=hit['_source']['content'],
                score=hit['_score']
            ) for hit in response['hits']['hits']]
            return Recommendations(recommendations=results)
        else:
            raise HTTPException(status_code=404, detail="No recommendations found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

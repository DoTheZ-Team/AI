from fastapi import APIRouter, Body
from models.recommend_model import RecommendationRequest
from db.database import es_client
import services.recommend_service as recommendsvs
from typing import List

recommends_router = APIRouter()

# 추천 결과 반환 API
@recommends_router.post("", response_model=List[int], summary="블로그 추천", description="블로그 id값과 팔로우된 블로그들의 정보를 바탕으로 블로그 추천을 해주는 API입니다. \n 블로그 서비스와 통신을 진행할 API입니다.")
async def recommend_blog(request: RecommendationRequest = Body(..., example={
        "blogId": "1",
        "followIds": ["2", "3"]
    })):
    
    # # # # 혹시나 인덱스 삭제 후 생성할 때 사용하기 위해 둔 부분
    # tfidf_matrix, vectorizer = tfidfsvs.TF_IDF()
    # es_client = await tfidfsvs.index_creation(tfidf_matrix)
    # docs = tfidfsvs.prepare_documents(tfidf_matrix)
    # await tfidfsvs.indexing(docs, es_client)

    response = await recommendsvs.recommend(request.blogId, request.followIds, es_client)
    
    recommend_blog_ids = [hit['_source']['blog_id'] for hit in response['hits']['hits']]
        
    return recommend_blog_ids
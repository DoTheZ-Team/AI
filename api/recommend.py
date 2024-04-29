from fastapi import APIRouter, Form, HTTPException
import services.hashtag_service as svs
from db.database import es_client
from models.recommendation import Recommendation, Recommendations

router = APIRouter()

@router.get("/user/{member_id}/recommend", response_model=Recommendations)
async def recommend_user(member_id: int):
    # if(새로운 해시태그 추가): 아래의 함수 실행: 새로운 해시태그 추가 부분을 어떻게 진행해야 될지 몰라서 일단 보류
    # svs.update_hashtag(member_id, new_hashtag, res)
    # tf-idf 수행
    tfidf_matrix, data = svs.TF_IDF()
    es_client = svs.index_creation(tfidf_matrix)
    docs = svs.prepare_documents(tfidf_matrix)
    svs.indexing(docs, es_client)
   
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

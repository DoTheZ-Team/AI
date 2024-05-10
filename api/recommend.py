from fastapi import APIRouter, Form, HTTPException
import services.hashtag_service as svs
import services.tf_idf.tf_idf_service as tfidfsvs
from models.recommendation import Recommendation, Recommendations
from db.database import es_client

router = APIRouter()

# 추천 결과 반환 API
@router.get("/user/{member_id}/recommend", response_model=Recommendations)
async def recommend_user(member_id: int):
    tfidf_matrix, data, vectorizer = tfidfsvs.TF_IDF()
    es_client = await tfidfsvs.index_creation(tfidf_matrix)
    docs = tfidfsvs.prepare_documents(tfidf_matrix)
    await tfidfsvs.indexing(docs, es_client)

    
    response = await svs.recommend_user(member_id, es_client, vectorizer)
    
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

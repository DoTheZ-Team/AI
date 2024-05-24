from elasticsearch import AsyncElasticsearch, TransportError
from elasticsearch.exceptions import BadRequestError
from core.error_handling import ErrorHandler

async def recommend(blog_id: int, followed_ids: list, es_client: AsyncElasticsearch, top_k: int = 4):
    # blogid를 followsId 목록에 추가(이거 안해주면 쿼리 결과에 요청한 사용자가 포함되어 나옴)
    followed_ids.append(blog_id)
    
    # 사용자의 벡터를 가져오기
    try:
        query = {
            "query": {
                "term": {"blog_id": blog_id}
            }
        }
        response = await es_client.search(index='tfidf_vector_index', body=query)
        
        if response['hits']['total']['value'] == 0:
            ErrorHandler.raise_not_found_error()

        # 첫 번째 매칭된 문서의 벡터 사용
        blog_vector = response['hits']['hits'][0]['_source']['content_vector']
    except KeyError:
        ErrorHandler.raise_not_found_error()

    # 코사인 유사도를 이용한 검색 쿼리, 이미 팔로우한 사용자를 제외
    query = {
        "size": top_k,
        "query": {
            "bool": {
                "must_not": [
                    {"terms": {"blog_id": followed_ids}}
                ],
                "should": [
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'content_vector')",
                                "params": {"query_vector": blog_vector}
                            }
                        }
                    }
                ]
            }
        }
    }
    
    try:
        response = await es_client.search(
            index="tfidf_vector_index",
            body=query
        )
        if not response['hits']['hits']:
            print("쿼리 반환 결과 없음.")
            return None

        return response 
    except BadRequestError as e:
        if 'script_score script returned an invalid score [NaN]' in str(e):
            print("유사 사용자 없음")
        return None

    except TransportError as e:
        ErrorHandler.handle_transport_error(e)
    except Exception as e:
        return ErrorHandler.handle_generic_error(e)
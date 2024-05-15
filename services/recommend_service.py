import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import AsyncElasticsearch, TransportError
from elasticsearch.exceptions import BadRequestError
from core.error_handling import ErrorHandler

# TODO: 응답 사이즈 결정해주면 그대로 수정 예정!
async def recommend(member_id: int, followed_ids: list, es_client: AsyncElasticsearch, top_k: int = 10):
    # memberId를 followsId 목록에 추가(이거 안해주면 쿼리 결과에 요청한 사용자가 포함되어 나옴)
    followed_ids.append(member_id)
    
    # 사용자의 벡터를 가져오기
    try:
        query = {
            "query": {
                "term": {"member_id": member_id}
            }
        }
        response = await es_client.search(index='tfidf_vector_index', body=query)
        
        if response['hits']['total']['value'] == 0:
            ErrorHandler.raise_not_found_error()

        # 첫 번째 매칭된 문서의 벡터 사용
        user_vector = response['hits']['hits'][0]['_source']['content_vector']
    except KeyError:
        ErrorHandler.raise_not_found_error()

    # 코사인 유사도를 이용한 검색 쿼리, 이미 팔로우한 사용자를 제외
    query = {
        "size": top_k,
        "query": {
            "bool": {
                "must_not": [
                    {"terms": {"member_id": followed_ids}}
                ],
                "should": [
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'content_vector')",
                                "params": {"query_vector": user_vector}
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
        
        for hit in response['hits']['hits']:
            print(f'회원 ID: {hit["_source"]["member_id"]}, 해시태그 내용: {hit["_source"]["content"]}, 유사도: {hit["_score"]}')

        return response 
    except BadRequestError as e:
        if 'script_score script returned an invalid score [NaN]' in str(e):
            print("유사 사용자 없음")
        return None

    except TransportError as e:
        ErrorHandler.handle_transport_error(e)
    except Exception as e:
        return ErrorHandler.handle_generic_error(e)
    

async def update(user_id: str, new_content: str, es_client: AsyncElasticsearch):
    vectorizer = TfidfVectorizer()
    try: 
        # ElasticSearch에서 현재 인덱스의 모든 데이터 불러오기
        data, current_tfidf_matrix = await get_tfidf_matrix(es_client)

        # 새로운 내용을 데이터 프레임에 추가
        new_row = pd.DataFrame({
            'member_id': [user_id],
            'content': [new_content]
        })
        data = pd.concat([data, new_row], ignore_index=True)

        # TF-IDF 벡터 재계산
        new_tfidf_matrix = vectorizer.fit_transform(data['content'])

        # 새로운 사용자 데이터의 벡터 찾기
        new_vector = new_tfidf_matrix[-1].toarray().flatten().tolist()  # 마지막 행이 새로운 데이터의 벡터

        # 업데이트할 데이터 구성
        update_data = {
            "doc": {
                "content": new_content,
                "content_vector": new_vector
            }
        }

        # ElasticSearch에 사용자 데이터 업데이트
        await es_client.update(index='tf_idf_vector_inde', id=user_id, body=update_data)

        # 최신 데이터 프레임과 벡터라이저 반환
        return data, vectorizer
    
    except BadRequestError as e:
        return ErrorHandler.raise_bad_request_error(str(e))
    except TransportError as e:
        return ErrorHandler.handle_transport_error(e)
    except Exception as e:
        return ErrorHandler.handle_generic_error(e)


async def get_tfidf_matrix(es_client: AsyncElasticsearch, index_name: str = 'tf_idf_vector_index'):
    try: 
        # 모든 문서 검색
        query = {
            "size": 10000,  # 최대 문서 수(TODO: 사이즈를 지정해줘야되는듯..? 더 찾아봐야 함)
            "query": {
                "match_all": {}
            }
        }
        response = await es_client.search(index=index_name, body=query)

        # 검색된 문서에서 데이터 추출
        contents = []
        member_ids = []
        vectors = []

        for hit in response['hits']['hits']:
            source = hit['_source']
            member_ids.append(source['member_id'])
            contents.append(source['content'])
            vectors.append(source['content_vector'])

        # 데이터 프레임 생성
        data = pd.DataFrame({
            'member_id': member_ids,
            'content': contents
        })

        # 벡터 행렬 생성
        tfidf_matrix = np.array(vectors)

        return data, tfidf_matrix
    except TransportError as e:
        return ErrorHandler.handle_transport_error(e)
    except Exception as e:
        return ErrorHandler.handle_generic_error(e)

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import AsyncElasticsearch, TransportError, helpers
from elasticsearch.exceptions import BadRequestError
from core.error_handling import ErrorHandler

async def update(member_id: int, new_hashtags: str, es_client: AsyncElasticsearch):
    vectorizer = TfidfVectorizer()
    
    # 사용자의 벡터를 가져오기
    try:
        query = {
            "query": {
                "term": {"member_id": member_id}
            }
        }
        response = await es_client.search(index='tfidf_vector_index', body=query) 
               
        if response['hits']['total']['value'] == 0:
            # 사용자 벡터가 없으면 새로운 데이터 추가
            existing_content = ""
        else:
            existing_content = response['hits']['hits'][0]['_source']['content']
        
    except KeyError:
        ErrorHandler.raise_not_found_error()
        
    try: 
        # 새로운 해시태그를 기존 해시태그에 추가
        combined_content = existing_content + " " + new_hashtags
        print(f"기존 해시태그: {existing_content}, 새로운 해시태그: {new_hashtags}, 결합된 해시태그: {combined_content}")

        # ElasticSearch에서 현재 인덱스의 모든 데이터 불러오기
        data = await get_tfidf_matrix(es_client)

        # 새로운 내용을 데이터 프레임에 추가
        new_row = pd.DataFrame({
            'member_id': [member_id],
            'content': [combined_content]
        })
        data = pd.concat([data, new_row], ignore_index=True)

        # TF-IDF 벡터 재계산
        new_tfidf_matrix = vectorizer.fit_transform(data['content'])

        await es_client.indices.delete(index="tfidf_vector_index", ignore=[400, 404])
        await es_client.indices.create(
            index="tfidf_vector_index",
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "member_id": {
                            "type": "keyword"
                        },
                        "content": {
                            "type": "text"
                        },
                        "content_vector": {
                            "type": "dense_vector",
                            "dims": new_tfidf_matrix.shape[1]
                        }
                    }
                }
            }
        )

        # 새로운 데이터 일괄 삽입 준비
        actions = []
        for idx in range(len(data)):
            
            member_id = data['member_id'].iloc[idx]
            content = data['content'].iloc[idx]
            new_vector = new_tfidf_matrix[idx].toarray().flatten().tolist()
            
            action = {
                "_index": "tfidf_vector_index",
                "_source": {
                    "member_id": member_id,
                    "content": content,
                    "content_vector": new_vector
                }
            }
            
            actions.append(action)
            
        # 일괄 삽입
        await helpers.async_bulk(es_client, actions)

        # 최신 데이터 반환
        updated_data = [{
            "member_id": member_id,
            "content": combined_content
        }]
        
        return updated_data
    except helpers.BulkIndexError as e:
        print(f"Bulk indexing error: {e}")
        raise ErrorHandler.handle_unexpected_error(str(e))
    except BadRequestError as e:
        return ErrorHandler.raise_bad_request_error(str(e))
    except TransportError as e:
        return ErrorHandler.handle_transport_error(str(e))
    except Exception as e:
        return ErrorHandler.handle_generic_error(str(e))


async def get_tfidf_matrix(es_client: AsyncElasticsearch, index_name: str = 'tfidf_vector_index'):
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

        for hit in response['hits']['hits']:
            source = hit['_source']
            member_ids.append(source['member_id'])
            contents.append(source['content'])

        # 데이터 프레임 생성
        data = pd.DataFrame({
            'member_id': member_ids,
            'content': contents
        })
        
        return data
    except TransportError as e:
        return ErrorHandler.handle_transport_error(e)
    except Exception as e:
        return ErrorHandler.handle_generic_error(e)

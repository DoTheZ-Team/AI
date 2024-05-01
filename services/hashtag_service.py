# from app.services.query_function import find_hashtags
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch, helpers, TransportError
from elasticsearch.exceptions import BadRequestError
from db.database import es_client
            
            
# 사용자의 id를 이용해 작성한 post_id를 전부 받아온다.
# 받아온 post_id를 이용해 개별 post를 조회한다.
# 조회된 개별 post에서 해시태그만을 가져와 id에 매핑되는 하나의 문자열을 만든다.
# 1. 만약 불러온 문자열과 업데이트된 문자열이 동일하다면 바로 추천을 진행한다.
# 2. 만약 불러온 문자열과 업데이트된 문자열이 다르다면 elasticsearch업데이트를 진행한 후 추천을 진행한다.
# Load the dataset
    
async def find_hashtags(member_id):
    # Query to Elasticsearch to get hashtag by member_id
    res = await es_client.search(
        index="hashtags",  # Ensure that this index exists in Elasticsearch
        body={
            "query": {
                "term": {"member_id": member_id}
            }
        }
    )
    
    return res


# 현재 이거 다 에러뜨는 상태!!!
async def recommend_user(member_id: int, es_client: Elasticsearch):
    # Perform the search and await the result
    # 현재 해시태그채로 서버에 저장이 안되어있음. 그래서 find_hashtag 자체가 동작을 안함
    # 이거 나중에 api 연결하고 해결할 예정
    #res = await find_hashtags(member_id)

    # 이것도 api 연결되고 나서나 할 수 있을듯..
    # vectorizer = TfidfVectorizer()
    query_vector = vectorizer.transform(['음식']).toarray()[0].tolist()
    
    # Changed query
    script_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, doc['content_vector']) + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "collapse": {
            "field": "member_id"
            }
        }
    
    try:
        # Perform the search and await the response
        response = await es_client.search(
            index="tfidf_vector_index",
            body=script_query,
            size=10
        )
        # Check if the response is empty or null
        if not response['hits']['hits']:
            print("No results returned from query.")
            return None
        
        # Display results
        for hit in response['hits']['hits']:
            print(f'Member ID: {hit["_source"]["member_id"]}, Content: {hit["_source"]["content"]}, Score: {hit["_score"]}')

        return response  # or process the response to your desired format before returning
    except BadRequestError as e:
        print(f"Error executing search query: {str(e)}")
        if 'script_score script returned an invalid score [NaN]' in str(e):
            print("Script returned NaN. Terminating function.")
        return None
    except TransportError as e:
        print(f"Transport error: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
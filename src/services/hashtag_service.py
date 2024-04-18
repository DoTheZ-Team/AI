# from app.services.query_function import find_hashtags
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch, helpers, TransportError
from elasticsearch.exceptions import BadRequestError
from src.database import es_client  # Make sure to import your Elasticsearch client
            
            
# 사용자의 id를 이용해 작성한 post_id를 전부 받아온다.
# 받아온 post_id를 이용해 개별 post를 조회한다.
# 조회된 개별 post에서 해시태그만을 가져와 id에 매핑되는 하나의 문자열을 만든다.
# 1. 만약 불러온 문자열과 업데이트된 문자열이 동일하다면 바로 추천을 진행한다.
# 2. 만약 불러온 문자열과 업데이트된 문자열이 다르다면 elasticsearch업데이트를 진행한 후 추천을 진행한다.
# Load the dataset
data_path = 'final_dataset.csv'
data = pd.read_csv(data_path)

vectorizer = TfidfVectorizer()
    
# TF-IDF 수행 함수 -> 해당 함수를 통해 주어진 데이터를 TF-IDF로 변환한다.
# 만약 새로운 해시태그가 추가된 상태라면 무조건 모든 데이터에 대해 TF-IDF를 수행해야 함.

def update_hashtag(member_id:int, new_hashtag:str, res:Elasticsearch):
# 문서가 있는 경우 content 필드에 새 해시태그를 추가합니다.
    if res['hits']['total']['value'] > 0:
        # Elasticsearch 문서의 현재 내용을 가져옵니다.
        current_hashtag_doc = res['hits']['hits'][0]
        current_content = current_hashtag_doc['_source']['content']

        # 새로운 해시태그를 기존 내용에 추가합니다.
        updated_content = current_content + ' ' + new_hashtag
        
        # 문서를 업데이트 합니다.
        es_client.update(
            index="hashtags",
            id=current_hashtag_doc['_id'],
            body={
                "doc": {
                    "content": updated_content,
                    "updated_at": datetime.now()
                }
            }
        )
        print(f"새로운 해시태그가 추가되었습니다: {new_hashtag}")
        
        return updated_content

    else:
            # 새 문서를 생성합니다.
            new_hashtag_doc = {
                "member_id": member_id,
                "content": new_hashtag,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            es_client.index(index="hashtags", document=new_hashtag_doc)
            
            print(f"새로운 해시태그 문서가 생성되었습니다: {new_hashtag}")
            return new_hashtag_doc
        
def TF_IDF():
    # Compute TF-IDF
    tfidf_matrix = vectorizer.fit_transform(data['content'])
    
    return tfidf_matrix, data

def index_creation(tfidf_matrix:np.ndarray):
    # Define the index configuration with dense_vector type
    index_config = {
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
                    "type": "text"  # Changed from 'keyword' to 'text' for full-text search capabilities
                },
                "content_vector": {
                    "type": "dense_vector",
                    "dims": tfidf_matrix.shape[1]  # Set dimensions to the number of features in TF-IDF
                }
            }
        }
    }
    
    # Create the index
    es_client.indices.create(index='tfidf_vector_index', body=index_config, ignore=400)
    return es_client
    
def prepare_documents(tfidf_matrix:np.ndarray):
    # Prepare documents for indexing
    docs = [{
        "_index": "tfidf_vector_index",
        "_source": {
            "member_id": row['member_id'],
            "content": row['content'],
            "content_vector": tfidf_matrix[index].toarray().flatten().tolist()  # Convert CSR row to dense format and flatten to a list
        }
    } for index, row in data.iterrows()]
    
    return docs

async def indexing(docs:dict, es_client:Elasticsearch):
    # Bulk indexing the documents
    await helpers.bulk(es_client, docs)
    
# def find_hashtags(member_id):
#     # Query to Elasticsearch to get hashtag by member_id
#     res = es_client.search(
#         index="tfidf_vector_index",  # Make sure this is the correct index name
#         body={
#             "query": {
#                 "term": {"member_id": member_id}
#             }
#         }
#     )
    
#     return res
# 바뀐 find_hashtags 함수
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


async def recommend_user(member_id: int, es_client: Elasticsearch):
    # Perform the search and await the result
    # 현재 해시태그채로 서버에 저장이 안돼있음......... 그래서 find_hashtag 자체가 동작을 안함;;;
    # 대박... 이거 나중에 api 연결하고 해결해야될듯....
    #res = await find_hashtags(member_id)

    # Create the query vector from the hashtags content
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
# from app.services.query_function import find_hashtags
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch, helpers, TransportError, AsyncElasticsearch
from elasticsearch.exceptions import BadRequestError
from db.database import es_client

# 데이터 가져오는 함수가 필요함. 이거는 나중에 수정할 예정
data = pd.read_csv('final_dataset.csv')

def TF_IDF():
    vectorizer = TfidfVectorizer()
    
    # 받아온 데이터로 tf-idf 수행
    tfidf_matrix = vectorizer.fit_transform(data['content'])
    
    return tfidf_matrix, data, vectorizer

async def index_creation(tfidf_matrix:np.ndarray):
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
                    "type": "text" 
                },
                "content_vector": {
                    "type": "dense_vector",
                    "dims": tfidf_matrix.shape[1] 
                }
            }
        }
    }
    
    # Create the index
    await es_client.indices.create(index='tfidf_vector_index', body=index_config, ignore=400)
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

async def indexing(docs: list, es_client: AsyncElasticsearch):
    # 비동기 버전의 Elasticsearch 클라이언트 사용
    await helpers.async_bulk(es_client, docs)
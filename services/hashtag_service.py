# from app.services.query_function import find_hashtags
from sklearn.feature_extraction.text import TfidfVectorizer
from elasticsearch import Elasticsearch, TransportError
from elasticsearch.exceptions import BadRequestError
from db.database import es_client
            
    
async def find_hashtags(member_id):
    res = await es_client.search(
        index="hashtags",
        body={
            "query": {
                "term": {"member_id": member_id}
            }
        }
    )
    
    return res


async def recommend_user(member_id: int, es_client: Elasticsearch, vectorizer: TfidfVectorizer):

    # 임시 데이터
    query_vector = vectorizer.transform(['음식']).toarray()[0].tolist()
    
    script_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                    "script": {
                        "source": """
                        if (doc['content_vector'].size() == 0) return 0.0;
                        return cosineSimilarity(params.query_vector, 'content_vector');
                        """,
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "collapse": {
            "field": "member_id"
            }
        }
    
    try:
        response = await es_client.search(
            index="tfidf_vector_index",
            body=script_query,
            size=10
        )
        if not response['hits']['hits']:
            print("No results returned from query.")
            return None
        
        for hit in response['hits']['hits']:
            print(f'Member ID: {hit["_source"]["member_id"]}, Content: {hit["_source"]["content"]}, Score: {hit["_score"]}')

        return response 
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
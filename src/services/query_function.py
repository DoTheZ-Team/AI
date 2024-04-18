from elasticsearch import AsyncElasticsearch
from database import es_client
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

async def find_hashtags(self, member_id):
        # Query to Elasticsearch to get hashtag by member_id
        res = await es_client.search(
            index="hashtags",  # Make sure this is the correct index name
            body={
                "query": {
                    "term": {"member_id": member_id}
                }
            }
        )
        
        return res
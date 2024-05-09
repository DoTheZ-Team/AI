from elasticsearch import AsyncElasticsearch
from core.config import ES_URL, api_key

es_client = AsyncElasticsearch(
    ES_URL,
    api_key=api_key
)

async def close_elasticsearch():
    es_client.close()

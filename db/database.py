from elasticsearch import AsyncElasticsearch
from core.config import ES_URL

es_client = AsyncElasticsearch(ES_URL)

async def close_elasticsearch():
    await es_client.close()

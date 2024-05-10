from elasticsearch import AsyncElasticsearch
from core.config import ES_URL, api_key

from core.config import db_config


es_client = AsyncElasticsearch(
    db_config.host,
    api_key = db_config.apiKey
)

async def close_elasticsearch():
    await es_client.close()

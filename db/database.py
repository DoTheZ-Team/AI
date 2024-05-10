from elasticsearch import AsyncElasticsearch
from core.config import ES_URL, api_key

from core.config import config



# 올바른 경로를 통해 설정 값을 참조
es_config = config['propertySources'][0]['source']
es_client = AsyncElasticsearch(
    es_config['elasticsearch.host'],
    api_key=es_config['elasticsearch.apiKey']
)

async def close_elasticsearch():
    await es_client.close()

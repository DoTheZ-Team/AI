from elasticsearch import AsyncElasticsearch
from core.config import config

# config 서버에서 가져온 설정을 이용해 Elasticsearch 클라이언트를 생성
es_config = config['propertySources'][0]['source']

es_client = AsyncElasticsearch(
    es_config['elasticsearch.host'],
    api_key=es_config['elasticsearch.apiKey']
)

async def close_elasticsearch():
    await es_client.close()

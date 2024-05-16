from elasticsearch import AsyncElasticsearch
from core.error_handling import ErrorHandler
from core.config import config

try:
    # # config 서버에서 가져온 설정을 이용해 Elasticsearch 클라이언트를 생성
    # es_config = config['propertySources'][0]['source']

    # es_client = AsyncElasticsearch(
    #     es_config['elasticsearch.host'],
    #     api_key=es_config['elasticsearch.apiKey']
    # )
    es_config, api_key = config
    
    es_client = AsyncElasticsearch(
        es_config,
        api_key=api_key
    )

except KeyError as e:
    ErrorHandler.handle_key_error(e, "잘못된 설정 데이터입니다.")
except Exception as e:
    ErrorHandler.handle_unexpected_error(e, "Elasticsearch 클라이언트를 생성하는 동안 예상치 못한 오류가 발생했습니다.")

async def close_elasticsearch():
    try:
        await es_client.close()
    except Exception as e:
        ErrorHandler.handle_generic_error(e, "Elasticsearch 클라이언트를 종료하는 동안 예상치 못한 오류가 발생했습니다.")


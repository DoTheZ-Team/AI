import requests
from core.error_handling import ErrorHandler
import dotenv
import os

dotenv.load_dotenv('.env')

def get_config():
    try: 
        #response = requests.get(os.environ.get("CONFIG_URL"))
        response = requests.get("http://glue-config.glue-service.svc.cluster.local:8888/recommend-dev/default")

        print(response.json())
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        ErrorHandler.handle_requests_http_error(e, "서버에서 설정을 가져오는데 실패했습니다.")
    except requests.exceptions.RequestException as e:
        ErrorHandler.handle_requests_exception(e, "설정을 가져오는 동안 오류가 발생했습니다.")
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e, "설정을 가져오는 동안 예상치 못한 오류가 발생했습니다.")



config = get_config()
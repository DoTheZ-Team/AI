import requests

def get_config():
    config_url = "http://glue-config.glue-service.svc.cluster.local:8888/recommend-dev/default"
    response = requests.get(config_url)
    print(response.json())
    return response.json()

config = get_config()
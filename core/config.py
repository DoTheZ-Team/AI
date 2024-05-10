# config.py
from pydantic import BaseModel
import yaml

# class DatabaseConfig(BaseModel):
#     host: str
#     apiKey: str


# def load_config(path: str):
#     with open(path, 'r') as f:
#         loaded_yaml = yaml.safe_load(f)
#         db_config = DatabaseConfig(**loaded_yaml['elasticsearch'])
#     return db_config

# # Load configuration
# db_config = load_config('core/application.yml')

import requests

def get_config():
    config_url = "http://localhost:8888/recommend-service/default"
    response = requests.get(config_url)
    return response.json()

config = get_config()


    
# ES_URL = "https://8063c2e7a91f4814b6c492ee9cc9283c.us-west-2.aws.found.io:443"
# api_key = "M1VBZFhZOEJibng1TUN3SkFoOU06M09STnV1T2RRc0dvaVZCSWM4NEZTZw=="
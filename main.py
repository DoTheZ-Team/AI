from fastapi import FastAPI
from api.recommend import router as recommend_router
from db.database import es_client, close_elasticsearch
from py_eureka_client import eureka_client
from core.config import config

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    eureka_config = config['propertySources'][0]['source']
    await eureka_client.init_async(
        eureka_server=eureka_config['eureka.client.service-url.defaultZone'], 
        app_name="recommnedation-service",
        instance_port=8080)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()
    
app.include_router(recommend_router)

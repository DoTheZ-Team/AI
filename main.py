from fastapi import FastAPI
from api.recommend import router as recommend_router
from db.database import es_client, close_elasticsearch
from py_eureka_client import eureka_client

app = FastAPI()
eureka_server = "http://localhost:8761/eureka"

@app.on_event("startup")
async def startup_event():
    await eureka_client.init_async(
        eureka_server=eureka_server, 
        app_name="recommnedation-service",
        instance_port=8080)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()
    
app.include_router(recommend_router)

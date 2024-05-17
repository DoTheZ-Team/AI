from fastapi import FastAPI
from api.recommend import recommends_router
from api.update import updates_router
from db.database import es_client, close_elasticsearch
import uvicorn

app = FastAPI(
    title="Recommend-Service", 
    openapi_url=f"/recommends/openapi.json")

@app.on_event("startup")
async def startup_event():
    print(await es_client.info())
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()
    
# 라우터 등록
app.include_router(recommends_router, prefix="/recommends")
app.include_router(updates_router, prefix="/recommends")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084)


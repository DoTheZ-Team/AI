from fastapi import FastAPI
from api.recommend import router as recommend_router
from db.database import es_client, close_elasticsearch
import uvicorn

app = FastAPI(
    title="Recommend-Service")

@app.on_event("startup")
async def startup_event():
    print(await es_client.info())
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()
    
app.include_router(recommend_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8080)
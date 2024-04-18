from fastapi import FastAPI
from src.api.user_routes import router as user_router
from src.database import es_client, close_elasticsearch

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_elasticsearch()
    
app.include_router(user_router)

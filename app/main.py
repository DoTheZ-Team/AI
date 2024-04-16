from fastapi import FastAPI
from api.user_routes import router as user_router
from database import mongodb

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    mongodb.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await mongodb.close()
    
app.include_router(user_router, prefix="/api")
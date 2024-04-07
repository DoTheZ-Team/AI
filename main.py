from fastapi import FastAPI, Form
from service.hashtag_service import Controller
from models import mongodb

app = FastAPI()
controller = Controller()

@app.on_event("startup")
def on_app_start():
	mongodb.connect()

@app.on_event("shutdown")
async def on_app_shutdown():
	mongodb.close()

# 해시태그 생성 및 업데이트
@app.post("/user/hashtag/update")
async def update_hashtag(member_id: int = Form(), content: str = Form()):
	hashtag = await controller.update_hashtag(member_id, content)
	return hashtag

# 해시태그 기반 유저추천
@app.get("/user/{member_id}/recommend")
async def recommend_user(member_id: int):
    recommend_user = await controller.recommend_user(member_id)
    return recommend_user
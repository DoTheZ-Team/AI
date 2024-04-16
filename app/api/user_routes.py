from fastapi import APIRouter, Form
from services.hashtag_service import Controller
from database import mongodb

router = APIRouter()
controller = Controller()

@router.post("/user/hashtag/update")
async def update_hashtag(member_id: int = Form(), content: str = Form()):
    hashtag = await controller.update_hashtag(member_id, content)
    return hashtag

@router.get("/user/{member_id}/recommend")
async def recommend_user(member_id: int):
    recommend_user = await controller.recommend_user(member_id)
    return recommend_user

# motor - MongoDB 용 비동기 python 라이브러리
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

# Secrets.json에서 MongoDB 정보를 가져옴.
from config.config import MONGO_DB_NAME, MONGO_DB_URL

# 몽고디비 연결
class MongoDB:
    def __init__(self):
        self.client = None
        self.client = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_DB_URL)
        self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
        print("DB와 연결되었습니다.")
    
    def close(self):
        self.client.close()

mongodb = MongoDB()
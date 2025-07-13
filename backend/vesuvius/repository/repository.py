from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.environ['MONGO_URI'])
db = client["prod"]

class Repository:
    COLLECTION = None
    MODEL = None

    @classmethod
    async def find(cls, *args, length=None, **kwargs):
        data = await cls.COLLECTION.find(*args, **kwargs).to_list(length=length)
        return [cls.MODEL(**item) for item in data]
  
    @classmethod
    async def find_one(cls, *args, **kwargs):
        return cls.MODEL(**await cls.COLLECTION.find_one(*args, **kwargs))
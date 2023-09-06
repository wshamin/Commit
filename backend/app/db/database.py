import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

client = AsyncIOMotorClient(MONGO_URI)

db = client['commit']

user_collection = db['users']
training_collection = db['trainings']
training_access_collection = db['training_accesses']
lesson_collection = db['lessons']

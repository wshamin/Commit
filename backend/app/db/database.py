from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb://127.0.0.1:27017')

db = client['commit']

user_collection = db['users']
course_collection = db['courses']
review_collection = db['reviews']

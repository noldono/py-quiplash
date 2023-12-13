from flask import Flask
from .config import *
from gamedb.mongo import MongoUserRepository, MongoGameRepository
from pymongo import MongoClient

MONGO_URL = MONGO_URL

app = Flask(__name__)

mongo_client = MongoClient(MONGO_URL)
user_repository = MongoUserRepository(mongo_client)
game_repository = MongoGameRepository(mongo_client)

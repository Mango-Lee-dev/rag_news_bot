from pymongo import MongoClient
import datetime

client = MongoClient(host="localhost", port=27017)

db = client['test']

collection = db['NewsText']

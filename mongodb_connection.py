from pymongo import MongoClient
import datetime

client = MongoClient(host="localhost", port=27017)

db = client['test']

collection = db['NewsText']

# item = {
#   "title": "심성전자 주가 일시 상승",
#   "text": "삼성전자 주가가 일시적으로 상승했다. 장중 최고치는...",
#   "date": datetime.datetime.now()
# }

# insert_id = collection.insert_one(item).inserted_id

print(collection.find_one())
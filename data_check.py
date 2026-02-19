from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

db = client['project1']
collection = db['newsAnalysis']

result = collection.find()

for item in result:
  print(item)
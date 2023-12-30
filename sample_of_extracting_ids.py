import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Recommender_sys']
collection = db['Books']

unique_asins = set()

with open('C:\\Users\\obeid\\Desktop\\Data Engineering\\Research\\Books_5.json') as file:
    for line in file:
        entry = json.loads(line)
        
        if entry['asin'] not in unique_asins:
            collection.insert_one({'Product_ID': entry['asin']})
            
            unique_asins.add(entry['asin'])

client.close()

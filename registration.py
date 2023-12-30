from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['Recommender_sys']
users_collection = db['Users']

def unique_id():
    return str(ObjectId())

users_collection.create_index([('email', 1)], unique=True)


inputs = {
    'user_id': unique_id(),
    'First_name': input("Enter your first name: "),
    'Last_name': input("Enter your last name: "),
    'email': input("Enter your email: "),
    'age': int(input("Enter your age: ")),
    'password': input("Enter your password: "),
    'Logged_in': False
}

users_collection.insert_one(inputs)



from pymongo import MongoClient
import time
client = MongoClient('mongodb://localhost:27017/')
db = client['Recommender_sys']

collections = [
    'Appliances',
    'Arts_Crafts_And_Sewing',
    'Automotive',
    'Beauty',
    'Books',
    'CDs_and_Vinyl',
    'Cell_Phones_and_Accessories',
    'Clothing_Shoes_and_Jewelry',
    'Digital_Music',
    'Electronics',
    'Fashion',
    'Gift_Cards',
    'Grocery_and_Gourmet_Food',
    'Home_and_Kitchen',
    'Industrial_and_Scientific',
    'Kindle_Store',
    'Luxury_Beauty',
    'Magazine_Subscriptions',
    'Movies_and_TV',
    'Musical_Instruments',
    'Office_Products',
    'Patio_Lawn_and_Garden',
    'Pet_Supplies',
    'Prime_Pantry',
    'Software',
    'Sports_and_Outdoors',
    'Tools_and_Home_Improvement',
    'Toys_and_Games',
    'Video_Games'
]

def matching_and_updating_IDs (user_interests):
    user_prefs = user_interests['interests']
    users_conn = db['Users']

    for collection in collections:
        conn_to_DB = db[collection]
        match_counts = conn_to_DB.aggregate([
            {
                '$match': {
                    'Product_ID': {'$in': user_prefs}
                }
            },
            {
                '$count': 'Count'
            }
        ])

        count = 0
        for matched_counts in match_counts:
            count = matched_counts['Count']
            break
        
        users_conn.update_one(
            {'user_id': user_interests['user_id']},
            {'$addToSet': {
                'categories': {
                    'name': collection,
                    'count': count
                }
            }}
        )

def return_items_based_on_user_prefs(user_details):
    sampled_documents = db['Review_Data'].aggregate([
        {'$sample': {'size': 5}},
        {'$project': {'asin': 1}}
        ])
    

    for category in user_details['categories']:
        total_count_of_interests = sum(category['count'] for category in user_details['categories'])

        percentage_of_interest = (category['count'] / total_count_of_interests)

        recommended_sample_items = db[str(category['name'])].aggregate([
            {'$sample': {'size': int(percentage_of_interest * 25)}},
            {'$project': {'Product_ID': 1, 'avg_reviews': 1}},
            {'$match': {'avg_reviews': {'$gt': 4}}}
        ]) 

        for recommended_item in recommended_sample_items:
            print(recommended_item['Product_ID'] + ' -> ' + category['name'])

    for random_sample_items in sampled_documents:
        print(random_sample_items['asin'])

def return_random_items():
    random_items = db['Review_Data'].aggregate([
    {'$sample': {'size': 30}},
    {'$project': {'asin': 1}}
    ])

    for random_item in random_items:
        print(random_item['asin'])

def main():
    user_interest = db['Users']

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = user_interest.find_one({'email': email, 'password': password})

    if user:
        user_id = user['_id']
        print("Login successful!")
        interests = []

        if user['Logged_in'] != True:
            user_interest.update_one({"_id": user_id}, {'$set': {'Logged_in': True}})
            
            return_random_items()

            while True:
                selection = input("Awaiting user selection...")

                if selection == 'x':
                    user_interest.update_one(
                        {'_id': user_id},
                        {'$set': {'interests': interests}}
                    )
                    client.close()
                    break
                else:
                    interests.append(selection) 
            

        else:
            matching_and_updating_IDs(user)
            return_items_based_on_user_prefs(user)
            
            while True:
                selection = input("Awaiting user selection...")

                if selection == 'x':
                    client.close()
                    break
                else:
                    interests.append(selection)
                    user_interest.update_one(
                        {'_id': user_id},
                        {'$addToSet': {'interests': selection}}
                    )


    else:
        print("Login failed. Invalid email or password.")

if __name__ == "__main__":
    main()

    

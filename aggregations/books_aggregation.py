from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Recommender_sys']

pipeline = [
    {
        '$lookup': {
            'from': 'Review_Data',
            'localField': 'Product_ID',
            'foreignField': 'asin',
            'as': 'All_overall',
            'pipeline': [
                {
                    '$project': {
                        'overall': '$overall',
                        '_id': 0
                    }
                }
            ]
        }
    },
    {
        '$addFields': {
            'avg_reviews': {'$trunc': [{'$avg': "$All_overall.overall"}, 2]}
        }
    },
    {
        '$out': 'Books' 
    }
]

result = db.Books.aggregate(pipeline)
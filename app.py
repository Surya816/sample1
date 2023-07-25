from flask import *
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017')
db = client['csv_data']
collection = db['class_register']

# @app.route('/')
# def index():
#     return send_from_directory('src/routes','+page.svelte')
@app.route('/api/data', methods=['GET'])
def get_data():
    result = []
    cursor = collection.find({})
    for doc in cursor:
        result.append({
            'first_name': doc['first_name'],
            'last_name': doc['last_name'],
            'company_name': doc['company_name'],
            'address': doc['address'],
            'city': doc['city'],
            'county': doc['county'],
            'state': doc['state'],
            'zip': doc['zip'],
            'phone1': doc['phone1'],
            'phone2': doc['phone2'],
            'email': doc['email'],
            'web': doc['web'],
            'date': doc.get('date','')
        })

    return jsonify(result)


@app.route('/api/filtered-data', methods=['GET'])
def get_filtered_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # start_date = request.args.get('startDate')
    # end_date = request.args.get('endDate')

    query = {}

    if start_date and end_date:

        start_datetime = datetime.strptime(start_date, '%d-%m-%Y %H:%M:%S')
        
        end_datetime =   datetime.strptime(end_date, '%d-%m-%Y %H:%M:%S')
        query = {
    'date': {
        '$gte': start_datetime,
        '$lte': end_datetime
    }
}
    
    result = []
    cursor = collection.find(query)
    for doc in cursor:
        result.append({
            'first_name': doc['first_name'],
            'last_name': doc['last_name'],
            'company_name': doc['company_name'],
            'address': doc['address'],
            'city': doc['city'],
            'county': doc['county'],
            'state': doc['state'],
            'zip': doc['zip'],
            'phone1': doc['phone1'],
            'phone2': doc['phone2'],
            'email': doc['email'],
            'web': doc['web'],
            'date': doc.get('date','')
        })

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug = True)

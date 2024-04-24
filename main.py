from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
import logging

app = Flask(__name__)
try:
    # Attempt to connect to the MongoDB Atlas cluster
    client = MongoClient('mongodb+srv://someshbhosale2:somesh@cluster0.atanct9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['synchronisation']  # Database name
    collection = db['hospitalData']
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("Error connecting to MongoDB Atlas:", e)

logging.basicConfig(level=logging.DEBUG)

# Define the hospital schema
hospital_schema = {
    "hospital_id": ObjectId,
    "name": str,
    "address": {
        "street": str,
        "city": str,
        "state": str,
        "zip_code": str
    },
    "contact": {
        "phone": str,
        "email": str
    },
    "doctors": [
        {
            "name": str,
            "specialization": str,
            "department": str,
            "contact": {
                "phone": str,
                "email": str
            }
        }
    ],
    "patients": [
        {
            "name": str,
            "age": int,
            "gender": str,
            "admission_date": str,
            "doctor": str,
            "condition": str
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/synchronize', methods=['GET'])
def synchronize():
    return render_template('synchronize.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['jsonFile']
        if file.filename.endswith('.json'):
            data = json.load(file)
            # Iterate over each document in the JSON data and insert into MongoDB collection
            for document in data:
                collection.insert_one(document)
            logging.info("Hospital data stored in the database")
            return jsonify({'message': 'Hospital data stored in the database'})
        else:
            logging.error("Invalid file format")
            return jsonify({'error': 'Invalid file format'})
    except Exception as e:
        logging.error("Error uploading hospital data: %s", e)
        return jsonify({'error': 'Error uploading hospital data'})

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    try:
        # Retrieve all hospital data from MongoDB collection
        data = list(collection.find({}))
        # Convert ObjectId to string for _id fields
        for document in data:
            document['_id'] = str(document['_id'])
        logging.info("Hospital data retrieved from the database")
        return jsonify({'data': data})  # Convert to JSON and return as an object with 'data' key
    except Exception as e:
        logging.error("Error retrieving hospital data from the database: %s", e)
        return jsonify({'error': 'Error retrieving hospital data from the database'})
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from firebase_admin import credentials, firestore, initialize_app
from model import Test
import os

# creating the flask app
app = Flask(__name__)

# creating an API object
api = Api(app)
cloud = os.environ.get('cloud')
key_path = '/firebase-key/latest-key' if cloud else 'db_key.json'

# Initializing Firestore Database
cred = credentials.Certificate(key_path)
default_app = initialize_app(cred)
db = firestore.client()
test_ref = db.collection('tests')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.String,
    'end': fields.String
}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class TestList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        try:
            # Check if ID was passed to URL query
            test_id = request.args.get('id')
            if test_id:
                test = test_ref.document(test_id).get()
                return test.to_dict(), 200
            else:
                all_tests = [doc.to_dict() for doc in test_ref.stream()]
                return all_tests, 200,
        except Exception as e:
            return f"An Error Occured: {e}", 400


class Test(Resource):
    @marshal_with(resource_fields)
    def post(self, test_id):
        try:
            # Overwrite entry if it exists, create it otherwise
            test_ref.document(test_id).set(request.json)
            return {'success': True}, 201
        except Exception as e:
            return f"An Error Occured: {e}", 400

    def delete(self, test_id):
        try:
            # Remove the entry with id test_id
            test_ref.document(test_id).delete()
            return {"success": True}, 204
        except Exception as e:
            return f"An Error Occured: {e}", 400

    def put(self, test_id):
        pass


api.add_resource(TestList, '/tests')
api.add_resource(Test, '/tests/<test_id>')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')

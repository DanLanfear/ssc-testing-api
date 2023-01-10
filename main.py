from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from firebase_admin import credentials, firestore, initialize_app
from model import Test
import os

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

# Initializing Firestore Database
cred = credentials.Certificate('/firebase-key/latest-key')
default_app = initialize_app(cred)
db = firestore.client()
test_ref = db.collection('tests')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.String,
    'end': fields.String
}

# Test resource


class Tests(Resource):
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
                return all_tests, 200, {'Access-Control-Allow-Origin': '*'}
        except Exception as e:
            return f"An Error Occured: {e}"

    def options(self):
        return 201, {'Access-Control-Allow-Origin': '*',
                     'Access-Control-Allow-Methods': 'POST,GET,DELETE',
                     'Access-Control-Allow-Headers': '*'}

    def post(self):
        try:
            id = request.json['id']
            print(request.json)
            test_ref.document(id).set(request.json)
            print(request.json)
            return {"success": True}, 200, {'Access-Control-Allow-Origin': '*'}
        except Exception as e:
            return f"An Error Occured: {e}"

    def delete(self):
        try:
            # Check for ID in URL query
            test_id = request.args.get('id')
            test_ref.document(test_id).delete()
            return {"success": True}, 200, {'Access-Control-Allow-Origin': '*'}
        except Exception as e:
            return f"An Error Occured: {e}"


api.add_resource(Tests, '/tests')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')

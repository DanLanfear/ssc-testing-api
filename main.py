# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from firebase_admin import credentials, firestore, initialize_app
from model import Test

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

cred = credentials.Certificate('db_key.json')
default_app = initialize_app(cred)
db = firestore.client()
test_ref = db.collection('tests')

resource_fields = {
    'name': fields.String,
    'start': fields.String,
    'end': fields.String
}


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
                return all_tests, 200
        except Exception as e:
            return f"An Error Occured: {e}"
        # return tests


class Test(Resource):
    @marshal_with(resource_fields)
    def post(self):
        try:
            id = request.json['id']
            test_ref.document(id).set(request.json)
            print(request.json)
            return request.json, 200
        except Exception as e:
            return f"An Error Occured: {e}"

    def delete(self):
        try:
            # Check for ID in URL query
            test_id = request.args.get('id')
            test_ref.document(test_id).delete()
            return jsonify({"success": True}), 200
        except Exception as e:
            return f"An Error Occured: {e}"


# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):

        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):

        data = request.get_json()     # status code
        return jsonify({'data': data}), 201

  # another resource to calculate the square of a number


# class Square(Resource):

#     def get(self, num):

#         return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
# api.add_resource(Square, '/square/<int:num>')
api.add_resource(Tests, '/tests')
api.add_resource(Test, '/test')


# driver function
if __name__ == '__main__':

    app.run(debug=True)

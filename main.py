# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from model import Test

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


tests = [
    Test(1, "dan", "1", "2"),
    Test(2, "george", "2", "3")
]

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.String,
    'end': fields.String
}


class Test(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return tests


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


class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')
api.add_resource(Test, '/tests')


# driver function
if __name__ == '__main__':

    app.run(debug=True)

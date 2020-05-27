# Methodology adapted from Melvin L
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"about":"Hello World!"}
    
    def post(self): 
        someJson = request.get_json()
        return {"you sent": someJson}, 201
    
class Multi(Resource):
    def get(self, num):
        return {"result": num*10}

# Routes 
api.add_resource(HelloWorld, "/")
api.add_resource(Multi, "/multi/<int:num>")

if __name__ == "__main__":
    app.run(debug=True)

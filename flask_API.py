# Methodology adapted from Melvin L
from flask import Flask,jsonify,  request
from flask_restful import Resource, Api
from main import JobSearch

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        # return {"about":"Hello World!"}
        args = request.args
        jobTitle = args["title"]
        jobLocation = args["loc"]
        jobRadius = args["rad"]
        newSearch = JobSearch()
        results = newSearch.search(jobTitle, jobLocation, jobRadius)
        # results.to_csv("./data/testFlask.csv", index=False)
        # print(results.to_json)
        # return {"you sent": someJson}, 201
        print(results)
        # results.headers.add('Access-Control-Allow-Origin', '*')
        # results.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        # results.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return results, 201
    
    def post(self): 
        newSearch = JobSearch()
        results = newSearch.search("Tester", "MA 02155", "10")
        results.to_csv("./data/testFlask.csv", index=False)
        # return {"you sent": someJson}, 201
        return jsonify(results), 201
    
class Multi(Resource):
    def get(self, num):
        return {"result": num*10}

# Routes 
api.add_resource(HelloWorld, "/")
api.add_resource(Multi, "/multi/<int:num>")

if __name__ == "__main__":
    app.run(debug=True)

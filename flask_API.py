# Methodology adapted from Melvin L
from flask import Flask,jsonify, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from main import JobSearch
from main import testMaps

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,c
#         'headers': {
#             'Access-Control-Allow-Headers': 'Content-Type',
#             'Access-Control-Allow-Origin': 'https://www.example.com',
#             'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
#         },
#         'body': json.dumps('Hello from Lambda!')
#     }

class HelloWorld(Resource):
    def get(self):
        args = request.args
        jobTitle = args["title"]
        jobLocation = args["loc"]
        jobRadius = args["rad"]
        newSearch = JobSearch()
        results = newSearch.search(jobTitle, jobLocation, jobRadius)
        # print(results)
        # results["center"]["Lng"], results["center"]["Lat"], results["center"]["Address"] = testMaps(CompanyLocation=jobLocation)
        # print(results["center"]["Lng"], results["center"]["Lat"], results["center"]["Address"])
        # results.to_csv("./data/testFlask.csv", index=False)
        # print(results.to_json)
        return results, 201
        
    # def post(self): 
    #     newSearch = JobSearch()
    #     results = newSearch.search("Tester", "MA 02155", "10")
    #     results.to_csv("./data/testFlask.csv", index=False)
    #     # return {"you sent": someJson}, 201
    #     return jsonify(results), 201

class Home(Resource):
    def get(self):
        return render_template('index.html')
    
class Multi(Resource):
    def get(self, num):
        return {"result": num*10}

# Routes 
api.add_resource(Home, "/")
api.add_resource(HelloWorld, "/search")
api.add_resource(Multi, "/multi/<int:num>")

if __name__ == "__main__":
    app.run(debug=True)



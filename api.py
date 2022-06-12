from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
app = Flask(__name__)
api = Api(app)

class MemberData(Resource):
    def get(self):
        with open("data/memberdata.json", "r") as infile:
            data = json.load(infile)
            return {"data" : data}, 200

api.add_resource(MemberData, '/memberdata')

if __name__ == '__main__':
    app.run()  # run our Flask app
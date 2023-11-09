from flask import Flask
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

db="celestrak_tle_data.csv"




class Main(Resource):
    def get(self):
          with open(db, 'r') as file:
            content = file.read()
            return content
    

api.add_resource(Main, "/api")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True,port=1000,host="127.0.0.1")

#    
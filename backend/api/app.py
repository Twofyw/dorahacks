from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200

from collections import Counter
class Recommend(Resource):

    def get_user_recommendation(self, userid):
        return [[i for _ in range(100)] for i in range(3)]

    def get(self):
        # TODO: num_results, userid
        userid = 0
        num_results = 10
        args = ['water', 'fat', 'carb']
        scores = [int(request.args.get(o)) for o in args]

        recommendations = self.get_user_recommendation(0)
        shuffle_batch(recommendations)
        gen_rec = merge_recommendations(recommendations, scores)
        return {'results': [next(gen_rec) for _ in range(num_results)]}
        # return "User not found", 404

import random
def shuffle_batch(recommendation, batch_size=10):
    """ 在长度为batch_size的片段内打乱结果，modify inplace

    """
    if len(recommendation) < batch_size:
        random.shuffle(recommendation)
        return

    for begin in range(len(recommendation) - batch_size):
        random.shuffle(recommendation[begin:begin + batch_size])
    return

import traceback
import random
import numpy as np
def merge_recommendations(recommendations, scores):
    for o in recommendations: shuffle_batch(o)
    p = [(100 - o) for o in scores]
    cumsum = np.cumsum(p)

    while True:
        r = random.random() * cumsum[-1]
        for i in range(3):
            if r < cumsum[i]:
                yield i
                break



api.add_resource(Recommend, "/api")

app.run(host='0.0.0.0', debug=True)


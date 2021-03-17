from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
# models imports
from models.user_model import *

model = UserModel()

class CreateUser(Resource):
    def post(self):
        pass

class GetUser(Resource):
    # @jwt_required
    def get(self):
       return model.get_user()
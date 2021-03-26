from flask_restful import Resource, abort
from flask import request, jsonify, make_response
from settings import ma
from marshmallow import ValidationError
from models.user_model import User

class Login(Resource):
    pass


class Logout(Resource):
    pass
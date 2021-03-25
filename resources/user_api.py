from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from settings import ma
from marshmallow import ValidationError

# models imports

from models.user_model import User
from models.appointment_model import Appointment
from models.guest_model import Guest
from models.image_model import Image

# schema imports
from schemas.user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserCollection(Resource):

    def get(self):
        """
        Get all users from the database: Je moet een admin zijn om dit te kunnen doen
        """
        users = User.get_all_users()
        return users_schema.dump(users)


    def post(self):
        """
        Add a new user to the database
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        succes, user = User.create(**data)
        if succes:
            return user_schema.dump(user), 201
        else:
            return 500
        

class UserApi(Resource):

    def get(self, user_id): 
        """
        get user based on userid
        """
        pass


    def put(self, user_id):
        """
        Edit user
        """
        pass

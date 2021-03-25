from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from settings import ma

# models imports

from models.user_model import User
from models.appointment_model import Appointment
from models.guest_model import Guest
from models.image_model import Image

# schema imports
from schemas.user_schema import UserSchema

# class CreateUserSchema(ma.Schema):
#     name = ma.fields.Str(required=True)
#     login = ma.fields.Str(required=True)
#     password = ma.fields.Str(required=True)
#     is_admin = ma.fields.Bool(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserCollection(Resource):

    def get(self):
        """
        Get all users from the database
        """
        users = User.get_all_users()
        print(users)
        users = users_schema.dump(users)
        print(users)
        return users


    def post(self):
        """
        Add a new user to the database
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = create_user_schema.load(json_data)
        except ma.ValidationError as err:
            return err.messages, 422
        
        videos[video_id] = data
        return videos[video_id], 201

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

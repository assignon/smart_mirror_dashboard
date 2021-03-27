from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from settings import ma
from marshmallow import ValidationError
from .authentication_api import login_required
# models imports

from models.user_model import User

# schema imports
from schemas.user_schema import UserSchema, EditUserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
edit_user_schema = EditUserSchema()


class UserCollection(Resource):
    @staticmethod
    @login_required
    def get(current_user):
        """
        Get all users from the database: Je moet een admin zijn om dit te kunnen doen
        """
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'})
        users = User.get_all_users()
        return users_schema.dump(users)

    @staticmethod
    @login_required
    def post(current_user):
        """
        Add a new user to the database
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # remove whitespaces from input
        
        remove_whitespace(json_data)

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


    def delete(self, user_id):
        User.delete_user(user_id)
        return 200


class UserApi(Resource):
    @staticmethod
    @login_required
    def get(current_user, user_id): 
        """
        get user based on userid
        """
        pass

    @staticmethod
    @login_required
    def put(current_user, user_id):
        """
        Edit user
        """

        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # remove whitespaces from input
        
        remove_whitespace(json_data)

        # Validate and deserialize input
        
        try:
            data = edit_user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        edited_user = User.update_user(user_id, **data)
        return user_schema.dump(edited_user), 200

                

def remove_whitespace(json_data):
    for key, value in json_data.items():
        if type(value) == str:
            json_data[key] = value.strip()

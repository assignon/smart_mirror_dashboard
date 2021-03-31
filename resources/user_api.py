from flask_jwt_extended import jwt_required
from flask_socketio import SocketIO, emit
from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma, db
from marshmallow import ValidationError
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from .authentication_api import login_required
from .helper import remove_whitespace
# models imports

# model = UserModel() 
class CreateUser(Resource):
    def post(self):
        pass

class GetUser(Resource):
    # @jwt_required
    def get(self):
        from app import socketio

        data = request.args
        socketio.emit('face_scanned',  data)
        
        return 'run'
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
        try: 
            users = User.get_all_users()
        except NoResultFound:
            return {'message': 'No users found in the database'}
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
        
        try: user = User.create(**data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return{'error': e.orig.args}
        
        return user_schema.dump(user), 201


    @staticmethod
    @login_required
    def delete(current_user, user_id):
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'})
        User.delete_user(user_id)
        return 200


class UserApi(Resource):

    @staticmethod
    @login_required
    def get(current_user, user_id): 
        """
        get user based on userid
        """
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'})

        try: 
            user = User.get_user(user_id)
        except NoResultFound:
            return{'message': 'User does not exist!'}

        return user_schema.dump(user), 200


        
    
    @staticmethod
    @login_required
    def put(current_user, user_id):
        """
        Edit user. Users can only edit their own user settings, exception is made for admins
        """
        if current_user.user_id != user_id and current_user.is_admin == False:
            return {"message": "Not authorized to edit this user!"}

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

        try:        
            edited_user = User.update_user(user_id, **data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return{'error': e.orig.args}
        except NoResultFound:
            return{'error': 'User does not exist'}
        return user_schema.dump(edited_user), 200

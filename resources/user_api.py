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


# # models imports

# # model = UserModel() 
# class CreateUser(Resource):
#     def post(self):
#         pass


# class GetUser(Resource):
#     # @jwt_required
#     def get(self):
#         from app import socketio

#         data = request.args
#         socketio.emit('face_scanned', data)

#         return 'run'


from models.user_model import User
# schema imports
# from schemas.user_schema import UserSchema, EditUserSchema, EditUserPasswordSchema
from schemas.schemas import UserSchema, EditUserSchema, EditUserPasswordSchema

user_schema: UserSchema = UserSchema()
user_response_schema = UserSchema(exclude=['password',])
users_response_schema = UserSchema(many=True, exclude= ['password',])
users_schema = UserSchema(many=True)
edit_user_schema = EditUserSchema()
edit_user_password_schema = EditUserPasswordSchema()


class UserCollection(Resource):

    @staticmethod
    @login_required
    def get(current_user: User):
        """
        Get all users from the database: Je moet een admin zijn om dit te kunnen doen
        """
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'}), 401
        try:
            users = User.get_all_users()
        except NoResultFound:
            return {'message': 'No users found in the database'}, 400
        return {"users": users_response_schema.dump(users)}, 200

    @staticmethod
    @login_required
    def post(current_user: User):
        """
        Add a new user to the database
        """
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'}), 401

        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # remove whitespaces from input

        remove_whitespace(json_data['body'])

        # Validate and deserialize input
        print(json_data)
        try:
            data = user_schema.load(json_data['body'])
        except ValidationError as err:
            return err.messages, 422

        try:
            user = User.create(**data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}

        return {"user": user_response_schema.dump(user)}, 201

    @staticmethod
    @login_required
    def delete(current_user, user_id):
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'})
        
        try: 
            User.delete_user(user_id)
        except:
            return 400
        return 200


class UserApi(Resource):

    @staticmethod
    @login_required
    def get(current_user: User, user_id: int):
        """
        get user based on userid
        """
        if not current_user.is_admin:
            return jsonify({'message': 'Not authorized to perform this function'})

        try:
            user = User.get_user(user_id)
        except NoResultFound:
            return {'message': 'User does not exist!'}

        return {"user": user_response_schema.dump(user)}, 200

    @staticmethod
    @login_required
    def put(current_user: User, user_id: int):
        """
        Edit user. Users can only edit their own user settings, exception is made for admins
        """
        if current_user.user_id != user_id and current_user.is_admin is False:
            return {"message": "Not authorized to edit this user!"}

        json_data: dict = request.get_json()['data']
        if not json_data:
            return {"message": "No input data provided"}, 400

        # remove whitespaces from input

        remove_whitespace(json_data)

        if current_user.user_id == user_id:
            user_to_be_updated = current_user
        else:
            try: 
                user_to_be_updated = User.get_user(user_id)
            except NoResultFound:
                return {'message': 'User does not exist!'}

        try:
            if json_data['new_password'] != '' and user_to_be_updated.check_password(json_data['password']):
                data = edit_user_password_schema.load(json_data)
                data['password'] = data.pop('new_password')
            elif json_data['new_password'] != '' and not user_to_be_updated.check_password((json_data['password'])):
                return jsonify({'error': 'incorrect password'})
            else:
                json_data.pop('new_password', None)
                json_data.pop('password', None)
                data = edit_user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        try:
            edited_user = User.update_user(user_id, **data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}
        except NoResultFound:
            return {'error': 'User does not exist'}

        return {"user": user_schema.dump(edited_user)}, 200

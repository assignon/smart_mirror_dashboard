from flask import request, jsonify, make_response
from flask_restful import Resource, abort
import jwt
import datetime
from functools import wraps
from settings import app, ma
from models.user_model import User


def login_required(fun):
    @wraps(fun)
    def check_token(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        print('request headerrrr', request.headers['x-access-token'])
        print('tokkkeennn', token)
        if not token:
            return jsonify({'message': 'Token is missing!'}, 401)

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
            if current_user is None:
                return jsonify({'error': 'The user_id is invalid'})
        except Exception as e:
            print('excceepptttionnnn',e)
            return jsonify({'message': 'Token is invalid!'})

        return fun(current_user, *args, **kwargs)

    return check_token


class Login(Resource):

    @staticmethod
    def get():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response("Could not verify", 401, {'WWW-Authenticate': ' Basic realm="Login required!"'})

        user = User.query.filter_by(email=auth.username).first()

        if not user:
            return {'message': 'User does not exist'}

        if user.check_password(auth.password):
            try:
                token = jwt.encode(
                    {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                    app.config['JWT_SECRET_KEY']).decode('utf-8')
            except:
                token = jwt.encode(
                    {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                    app.config['JWT_SECRET_KEY'])
            return jsonify({'x-access-token': token})
        return make_response("Could not verify", 401, {'WWW-Authenticate': ' Basic realm="Login required!"'})


class Logout(Resource):
    pass

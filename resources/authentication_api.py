import os, smtplib, ssl, random, string
from dotenv import load_dotenv
from flask import request, jsonify, make_response, session
from flask_restful import Resource
import jwt
import datetime
from functools import wraps
from settings import app, db
from models.user_model import User


def login_required(fun):
    @wraps(fun)
    def check_token(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
            if current_user is None:
                return jsonify({'error': 'The user_id is invalid'})
        except Exception as e:
            return jsonify({'error': 'Token is invalid!'})

        return fun(current_user, *args, **kwargs)

    return check_token


class Login(Resource):

    @staticmethod
    def get():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response({"error": "Login information incomplete"},200, {'WWW-Authenticate': ' Basic realm="Login required!"'})

        try:
            user = User.query.filter_by(email=auth.username).first()
        except Exception:
            return {"error": "Database Server Error"}

        if not user:
            return {'error': 'User does not exist'}

        if user.check_password(auth.password):
            try:
                token = jwt.encode(
                    {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                    app.config['JWT_SECRET_KEY']).decode('utf-8')
            except:
                token = jwt.encode(
                    {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                    app.config['JWT_SECRET_KEY'])
            return jsonify({'x-access-token': token, 'user_id': user.user_id, 'superuser': user.is_admin})
        return make_response({"error": "Wrong password"}, 200, {'WWW-Authenticate': ' Basic realm="Login required!"'})


class Logout(Resource):
    @staticmethod
    @login_required
    def get(current_user):
        session.clear()
        return make_response({'logout': True})


class PasswordManager(Resource):

    @staticmethod
    def get():

        if not request.args:
            return {"error": "No input data provided"}
        email = request.args.get('email')
        if email is not None:
            try:
                user: User = db.session.query(User).filter_by(email=email).first()
                if user:
                    # email versturen met random token
                    # token = jwt.encode(
                    #         {'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                    #         app.config['JWT_SECRET_KEY']).decode('utf-8')
                    # send_email(user, token)
                    # sla de token op in redis voor 24 uur.
                    # redis_db.set(f"password_token:{user.user_id}", token, ex=int(time.time()) + 24*60*60)
                    # get random password pf length 8 with letters, digits, and symbols
                    password_characters = string.ascii_letters + string.digits + '!?'
                    new_password = ''.join(random.choice(password_characters) for _ in range(16))
                    try:
                        User.update_user(user.user_id, password=new_password)
                    except Exception:
                        return {"error": "Database Server Error"}
                    try:
                        send_email(user, new_password)
                        return {'message': 'New password has been sent to your email.'}
                    except Exception:
                        return {"error": "new_password has been created but email has not been send, because of an "
                                         "error "
                                         " in the email server"}
                else:
                    return {'error': 'This email is not recognized.'}
            except Exception:
                return {"error": "Database Server Error"}
        else:
            return {"error": "Email not provided in the data"}

    # @staticmethod
    # def post():
    #     json_data: dict = request.get_json()
    #     if not json_data:
    #         return {"message": "No json data provided"}, 400
    #
    #     if 'password_token' not in json_data.keys():
    #         return {"message": "password_token not provided in the data"}
    #
    #     try:
    #         token_data = jwt.decode(json_data['password_token'], app.config['JWT_SECRET_KEY'])
    #         user = User.query.filter_by(user_id=token_data['user_id']).first()
    #         if user is None:
    #             return jsonify({'message': 'The user_id is invalid'})
    #     except:
    #         return jsonify({'message': 'Token is invalid!'})
    #
    #     if json_data['password_token'] == redis_db.get(f"password_token:{user.user_id}").decode("utf-8"):
    #         users_response_schema = UserSchema(exclude=['password', ])
    #         return {"Authenticated": True, "user": users_response_schema.dump(user)}
    #     else:
    #         return {"message": "Token is invalid"}
    #
    # @staticmethod
    # def put():
    #     json_data: dict = request.get_json()
    #     if not json_data:
    #         return {"message": "No input data provided"}, 400
    #
    #     if 'password_token' not in json_data.keys():
    #         return {"message": "password_token not provided in the data"}
    #
    #     if 'new_password' not in json_data.keys():
    #         return {"message": "new_password missing :("}
    #
    #     try:
    #         token_data = jwt.decode(json_data['password_token'], app.config['JWT_SECRET_KEY'])
    #         user = User.query.filter_by(user_id=token_data['user_id']).first()
    #         if user is None:
    #             return jsonify({'message': 'The user_id is invalid'})
    #     except:
    #         return jsonify({'message': 'Token is invalid!'})
    #
    #     try:
    #         if json_data['password_token'] == redis_db.get(f"password_token:{user.user_id}").decode("utf-8"):
    #             User.update_user(user.user_id, password=json_data['new_password'])
    #             redis_db.delete(f"password_token:{user.user_id}")
    #             return {"message": "Password has been updated, you can now login with your new password"}
    #         else:
    #             return {"message": "Token is invalid"}, 200
    #     except:
    #         return {"message": "Token is invalid"}


load_dotenv('../.env')


def send_email(user, new_password):

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()
    sender = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        message = f"""\
        Subject: Change Password\n
        
        Hi {user.name}, You forgot your password :(\n 
        No worries! I made a new password just for you! :)\n
        You can change this password in your settings.\n
        \n
        New Password: {new_password}
        
        This message is sent from Python."""

        server.login(sender, password)
        server.sendmail(sender, user.email, message)

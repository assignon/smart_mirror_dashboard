from datetime import datetime
from settings import db, bcrypt
# from flask_bcrypt import generate_password_hash, check_password_hash
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import jsonify, make_response

# db = setting['db']

class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    login = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(length=30), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    
    # def __init__(self, name, login, password, is_admin):
    #     self.name = name
    #     self.login = login
    #     self.password = password
    #     self.is_admin = is_admin
    
    def __repr__(self):
        return str(self.name)
    
    def hash_pass(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf8')
        
    def check_pass(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def new_user(self):
        # add new user to DB
        pass

    def signin(self):
        # # login basis user sended data verification
        
        # # aad expiration time for the created user token 
        # expires = datetime.timedelta(days=1)
        # token = create_access_token(indentity=str(user.id), expires_delta=expires)
        # refresh_token = create_refresh_token(identity = str(user.id))
        
        # return {'token': token, 'user_id': user.id, 'admin': user.is_admin}
        pass
    
    def get_user(self):
        return jsonify(dict({'id': 1, 'name': 'Yanick', 'admin': True, 'token': 'wsdhj98743puihsadnv36'}))
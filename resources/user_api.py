from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_socketio import SocketIO, emit
# models imports
from models.user_model import *

model = UserModel() 
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
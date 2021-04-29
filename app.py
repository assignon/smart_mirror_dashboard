from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, send, ConnectionRefusedError, disconnect
# from flask_bcrypt import Bcrypt
from flask_restful import Api
from settings import app, rest_api
from routes import api_routes
import time

app.secret_key = "sunnySideUp-smartMirror"
# bcrypt = Bcrypt(app)
rest_api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='http://192.168.178.52:8080')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@socketio.on('connect')
def user_connect():
    authentcated = True
    # if not self.authenticate(request.args):
    if not authentcated:
        print('login')
        raise ConnectionRefusedError('unauthorized!')
    else:
        print('user connected')
        send({'msg': 'user connected'}, json=True)
        
@socketio.on('new_user')
def subscribe_user(data):
    """
    add user in SocketUserManager DB and socket

    Args:
        data (obj): [login user id]
    """
    # handle connected user to the socket
    print('daaatttaa', data)
    emit('user_joined', {'username': data['username']}, broadcast=True, include_self=False)
    # time.sleep(1)
    # disconnect()
    
@socketio.on('disconnect')
def user_disconnect():
    print('Client disconnected')
    send({'msg': 'user disconnected'})
    
@socketio.on('user_disconnected')
def unsubscribe_user(data):
    """
    remove user fron SocketUserManager DB and socket

    Args:
        data (obj): [logout user id]
    """
    print('diconnected use', data)
    

api_routes(rest_api)


if __name__ == 'main':
    socketio.run(app)
    # app.run()

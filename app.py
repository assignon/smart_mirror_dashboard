from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, send, ConnectionRefusedError, disconnect
from flask_cors import CORS
# from flask_bcrypt import Bcrypt
from flask_restful import Api
from settings import app, rest_api
from routes import api_routes
import time, datetime

app.secret_key = "sunnySideUp-smartMirror"
# bcrypt = Bcrypt(app)
rest_api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*')

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "Access-Control-Allow-Origin": "*"
    }
})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# @app.route('/')
# def index():
#     # return app.send_static_file('index.html')
#     return render_template("index.html")

# @app.route('/login')
# def index():
#     return app.send_static_file('index.html')

# @app.route('/ingecheckt')
# def ingecheckt():
#     return app.send_static_file('index.html')

# @app.route('/clients')
# def clients():
#     return app.send_static_file('index.html')

# @app.route('/instellingen')
# def instellingen():
#     return app.send_static_file('index.html')

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

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
    # emit('user_joined', {'username': data['username']}, broadcast=True, include_self=False)
    emit('user_joined', {'username': 'Yanick'}, broadcast=True)
    # time.sleep(1)
    # disconnect()
    
# @socketio.on('disconnect')
# def user_disconnect():
#     print('Client disconnected')
#     send({'msg': 'user disconnected'})
    
@socketio.on('user_disconnected')
def unsubscribe_user(data):
    """
    remove user fron SocketUserManager DB and socket

    Args:
        data (obj): [logout user id]
    """
    print('diconnected use', data)
    
@socketio.on('update_checkedin')
def update_checked_guest(guest_data):
    # now = datetime.datetime.now()
    emit('checked_in',  guest_data,
                        broadcast=True)
    
@socketio.on('update_checkedout')
def update_checked_guest(guest_data):
    # now = datetime.datetime.now()
    emit('checked_out',  guest_data,
                        broadcast=True)
    

api_routes(rest_api)


if __name__ == 'main':
    # socketio.run(app)
    print('test')
    app.run()

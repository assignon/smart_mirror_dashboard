from werkzeug.datastructures import Headers
from flask import Flask, render_template, request, session, redirect, url_for, Response
from flask_socketio import SocketIO, emit, send, ConnectionRefusedError, disconnect
from flask_cors import CORS
# from flask_bcrypt import Bcrypt
from flask_restful import Api
from settings import app, rest_api, PROJECT_DIR
from routes import api_routes
import time
import datetime
import os

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


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")


BUILD_DIR = PROJECT_DIR+'/frontend/dist'


def load_index_file():
    """
    load generated files(views) from vue build
    Returns:
        [file]: [vue views files]
    """
    # path to the vue build static file
    index_file_path = '{}/index.html'.format(BUILD_DIR)
    with open(index_file_path, 'r', encoding='utf-8') as f:
        index_file = f.read()
    return index_file


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
index_file = load_index_file()


@app.route('/', methods=['GET'])
def index():
    """render vue login page

    Returns:
        [file]: [get vue login static page]
    """
    return Response(index_file, mimetype='text/html',
                    headers=Headers({'Cache-Control': 'max-age=60'}))


@app.route('/ingecheckt', methods=['GET'])
def ingecheckt():
    """render vue in-uitcheck page

    Returns:
        [file]: [get vue in-uitcheck static page]
    """
    return Response(index_file, mimetype='text/html',
                    headers=Headers({'Cache-Control': 'max-age=60'}))


@app.route('/clients', methods=['GET'])
def clients():
    """render vue clients page

    Returns:
        [file]: [get vue clients static page]
    """
    return Response(index_file, mimetype='text/html',
                    headers=Headers({'Cache-Control': 'max-age=60'}))


@app.route('/admin', methods=['GET'])
def admin():
    """render vue admin page

    Returns:
        [file]: [get vue admin static page]
    """
    return Response(index_file, mimetype='text/html',
                    headers=Headers({'Cache-Control': 'max-age=60'}))


@app.route('/instellingen', methods=['GET'])
def instellingen():
    """render vue instellingen page

    Returns:
        [file]: [get vue instellingen static page]
    """
    return Response(index_file, mimetype='text/html',
                    headers=Headers({'Cache-Control': 'max-age=60'}))


@app.route('/<path:path>')
def static_file(path):
    """get static file collected from vue build

    Args:
        path ([str]): [flask route path]

    Returns:
        [file]: [vue static file]
    """
    return app.send_static_file(path)


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


if __name__ == '__main__':
    socketio.run(app)

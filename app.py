from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
# from flask_bcrypt import Bcrypt
from flask_restful import Api
from settings import app
from routes import api_routes

app.secret_key = "sunnySideUp-smartMirror"
# bcrypt = Bcrypt(app)
rest_api = Api(app)
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

api_routes(rest_api)


if __name__ == 'main':
    socketio.run(app)
    # app.run()




from flask import Flask, render_template, request, session, redirect, url_for
# from flask_bcrypt import Bcrypt
from flask_restful import Api
from settings import app
from routes import api_routes

app.secret_key = "sunnySideUp-smartMirror"
# bcrypt = Bcrypt(app)
rest_api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

api_routes(rest_api)


if __name__ == 'main':
    app.run()




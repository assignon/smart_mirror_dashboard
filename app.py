from flask import Flask, render_template, request, session, redirect, url_for
# from flask_bcrypt import Bcrypt
from settings import app, rest_api
from routes import api_routes

app.secret_key = "sunnySideUp-smartMirror"
# bcrypt = Bcrypt(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

api_routes(rest_api)


if __name__ == 'main':
    app.run()




from flask import Flask, render_template, request, session, redirect, url_for
# from flask_restful import Api

app = Flask(__name__, static_url_path='/static', template_folder="templates")
app.secret_key = "sunnySideUp-smartMirror"


@app.route('/')
def hello_world():
    return 'Hello, World!'


def run_app():
    app.run()


if __name__ == 'main':
    run_app()




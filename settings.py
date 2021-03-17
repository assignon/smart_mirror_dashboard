import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
# from flask_restful import Api
# if 'app' not in sys.modules:
#     from app import app 

app = Flask(__name__, static_url_path='/static', template_folder="templates")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
app.config.from_envvar('ENV_FILE_LOCATION')
bcrypt = Bcrypt(app)

## Db configurations
# sqlite conf
db_file = "sqlite:///{}".format(os.path.join(PROJECT_DIR, 'app.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['JWT_SECRETE_KEY'] = '8435dc97-3815-4cfe-aa96-007a52dc98b8'
# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# mysql conf


## api settings
# rest_api = Api(app)
# custom error

## jwt authentication setup
jwt = JWTManager(app)
# jwt._set_error_handler_callbacks(rest_api)
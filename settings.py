import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


# from flask_restful import Api
# if 'app' not in sys.modules:
#     from app import app



app = Flask(__name__, static_url_path='/static', template_folder="templates")

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Smart-Mirror-Dashboard-API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
app.config.from_envvar('ENV_FILE_LOCATION')
bcrypt = Bcrypt(app)

## Db configurations


import urllib

server = 'sunny-side-up.database.windows.net'
database = 'smart-mirror'
username = 'tientjie'
password = 'sunny-side-UP'
driver = 'ODBC Driver 17 for SQL Server'

params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=sunny-side-up.database.windows.net'
                                 ';DATABASE=smart-mirror;UID=tientjie;PWD=sunny-side-UP')
connection_url = "mssql+pyodbc:///?odbc_connect=%s" % params

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url

app.config['JWT_SECRET_KEY'] = '8435dc97-3815-4cfe-aa96-007a52dc98b8'

# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# mysql conf


## api settings
rest_api = Api(app)


# initialize marshmallow

ma = Marshmallow(app)

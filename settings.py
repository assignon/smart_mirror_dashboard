import os
import sys
import time
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_apscheduler import APScheduler
from RedisDB.redisdb import RedisDatabase
from daily import daily_delete
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# from flask_restful import Api
# if 'app' not in sys.modules:
#     from app import app


# app = Flask(__name__, static_url_path='/',
#             static_folder="../frontend/dist/", template_folder="templates")
# app = Flask(__name__, static_url_path='/static', template_folder="templates")
app = Flask(__name__, static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

# swagger specific
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


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
app.config.from_envvar('ENV_FILE_LOCATION')
bcrypt = Bcrypt(app)

# Db configurations

load_dotenv('.env')
"""AWS CONNECTIE"""
username = os.getenv('AWS_USERNAME')
password = os.getenv('AWS_PASSWORD')
host = os.getenv('AWS_HOST')
db_name = os.getenv('AWS_DB_NAME')

connection_url = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url

app.config['JWT_SECRET_KEY'] = '8435dc97-3815-4cfe-aa96-007a52dc98b8'

# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Redis connection
redis_db = RedisDatabase(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),
                         password=os.getenv('REDIS_PASSWORD'))

# api settings
rest_api = Api(app)


# initialize marshmallow

ma = Marshmallow(app)

# scheduling:


# def daily_task():
#     """Verwijder alle gasten die overdatum zijn"""
#     print("Deleting all expired guests....")
#     daily_delete(db, redis_db)


# scheduler = APScheduler()

# """Schedule configuratuons"""

# # check of de laatste taak geexecute is.

# res = db.session.execute(
#     """SELECT next_run_time FROM apscheduler_jobs;""").first()
# if res.next_run_time < time.time():
#     daily_task()

# # app.config['SCHEDULER_API_ENABLED'] = True
# app.config['JOBS'] = [{"id": "remove_expired_guests", "func": daily_task, 'replace_existing': True,
#                        "trigger": "cron", "hour": 0, "minute": 0, "second": 0}]

# app.config['SCHEDULER_JOBSTORES'] = {
#     "default": SQLAlchemyJobStore(url=connection_url)}

# scheduler.init_app(app)
# scheduler.start()

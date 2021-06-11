import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

try:
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    # from .base_model import BaseMixin
    from settings import app
except:
    from settings import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


manager.run()
import os
from flask.ext.alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from flask.ext.script import Manager
from flask import Flask
from flask_mail import Mail
from backend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask.json import JSONEncoder
from datetime import datetime
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.abspath(os.path.join(basedir, 'uploads'))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__,
            static_folder = basedir + "/dist/static",
            template_folder = basedir + "/dist")
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100*1024*1024
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
))
mail = Mail(app)

# init Alchemy Dumps
alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)
manager.add_command('db', MigrateCommand)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
app.json_encoder = CustomJSONEncoder

from backend import routes, models

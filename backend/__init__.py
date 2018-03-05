import os
from flask import Flask
from flask_mail import Mail
from backend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.json import JSONEncoder
from datetime import datetime

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,
            static_folder = basedir + "/dist/static",
            template_folder = basedir + "/dist")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'hanj417@gmail.com',
    MAIL_PASSWORD = 'dhsdb417',
))
mail = Mail(app)



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

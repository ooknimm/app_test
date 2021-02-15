from flask import Flask

from view import create_endpoints
from service import UserService
from utils.custom_json_encoder import CustomJSONEncoder


class Service:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    database = app.config['DB']

    services = Service
    services.user_service = UserService(app.config)

    create_endpoints(app, services, database)

    return app

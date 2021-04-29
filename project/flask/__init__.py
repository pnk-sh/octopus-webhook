import os
import dotenv
from flask import Flask
from flask_cors import CORS

from project.middleware.connect import Connect
from project.middleware.authIdentifier import AuthIdentifier

from project.flask.notifications import Notifications
from project.flask.identifiers import Identifiers

dotenv.load_dotenv()
debug_mode = True if os.getenv("DEBUG_MODE") == "1" else False


def create_app(config_filename=None, instance_relative_config=True):
    app = Flask(__name__)

    if config_filename is not None:
        app.config.from_pyfile(config_filename)

    CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.wsgi_app = AuthIdentifier(app.wsgi_app)
    app.wsgi_app = Connect(app.wsgi_app)

    app.add_url_rule(
        f"/webhook",
        view_func=Notifications.webhook,
        endpoint="notifications_webhook",
        methods=["POST"],
    )

    app.add_url_rule(
        f"/identifier",
        view_func=Identifiers.get_all,
        endpoint="identifier_get_all",
        methods=["GET"],
    )

    app.add_url_rule(
        f"/identifier",
        view_func=Identifiers.create,
        endpoint="identifier_create",
        methods=["POST"],
    )

    return app

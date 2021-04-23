  
import logging
logging.basicConfig(level=logging.INFO)

import os
from flask import Flask, request, Response
from flask_cors import CORS

from middleware.connect import Connect
from middleware.authIdentifier import AuthIdentifier

from libaray.flask.notifications import Notifications

app = Flask(__name__)
app.wsgi_app = AuthIdentifier(app.wsgi_app)
app.wsgi_app = Connect(app.wsgi_app)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

app.add_url_rule(f'/webhook', view_func=Notifications.webhook, endpoint='notifications_webhook', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
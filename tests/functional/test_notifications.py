from project.flask import create_app
from project.odm.webhook import Webhook as OdmWebhook


def test_notifications_create():
    OdmWebhook.drop_collection()

    app = create_app()

from datetime import datetime
from project.odm.webhook import Webhook
from bson.json_util import dumps, loads
from flask import Response, request
from mongoengine import DoesNotExist


class Notifications:
    @staticmethod
    def webhook():
        data = request.get_json()

        webhook_data = Webhook()
        webhook_data.identifier = request.args.get("identifier")
        webhook_data.webhook = data
        webhook_data.save()

        return (
            Response(
                dumps({"status": 200, "content": {"id": webhook_data.pk}}),
                mimetype="text/json",
            ),
            200,
        )

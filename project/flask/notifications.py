import os
import pika
from datetime import datetime
from project.odm.webhook import Webhook as OdmWebhook
from bson.json_util import dumps, loads
from flask import Response, request
from mongoengine import DoesNotExist


class Notifications:
    @staticmethod
    def webhook():
        data = request.get_json()

        webhook_data = OdmWebhook()
        webhook_data.identifier = request.args.get("identifier")
        webhook_data.webhook = data
        webhook_data.save()

        if os.getenv("RABBITMQ_ENABLE") == "1":
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"))
            )
            channel = connection.channel()
            channel.queue_declare(queue="webhook")
            channel.basic_publish(
                exchange="",
                routing_key="webhook",
                body=dumps(
                    {
                        "id": str(webhook_data.pk),
                        "identifier": webhook_data.identifier,
                        "tag": data["push_data"]["tag"],
                        "image": data["repository"]["repo_name"],
                    }
                ),
            )
            connection.close()

        return (
            Response(
                dumps({"status": 200, "content": {"id": webhook_data.pk}}),
                mimetype="text/json",
            ),
            200,
        )

    @staticmethod
    def get_webhook():
        args_status = request.args.get("status")
        query_filter = {}

        if args_status is not None:
            query_filter["status"] = args_status

        webhook_data = OdmWebhook.objects.aggregate(
            [
                {"$match": query_filter},
                {
                    "$project": {
                        "_id": 1,
                        "number": 1,
                        "status": 1,
                        "identifier": 1,
                        "image": "$webhook.repository.name",
                        "tag": "$webhook.push_data.tag",
                        "namespace": "$webhook.repository.namespace",
                        "pushed_at": "$webhook.push_data.pushed_at",
                    }
                },
            ]
        )

        return (
            Response(
                dumps({"status": 200, "content": webhook_data}),
                mimetype="text/json",
            ),
            200,
        )

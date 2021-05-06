import os
import pika
from datetime import datetime
from project.model.logging import insert_logging
from project.odm.webhook import Webhook as OdmWebhook
from bson.json_util import dumps, loads
from flask import Response, request


class Notifications:
    @staticmethod
    def webhook():
        data = request.get_json()

        webhook_data = OdmWebhook()
        webhook_data.identifier = request.args.get("identifier")
        webhook_data.webhook = data
        webhook_data.created_at = datetime.utcnow()
        webhook_data.save()

        insert_logging(
            summary='Webhook - success created',
            binds=[
                f'webook_id-{str(webhook_data.pk)}',
                f'webook_number-{webhook_data.number}',
                f'webook_identifier-{webhook_data.identifier}',
            ]
        )

        if os.getenv("RABBITMQ_ENABLE") == "1":
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                    int(os.getenv('RABBITMQ_PORT')),
                    os.getenv('RABBITMQ_VHOST'),
                    pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS')))
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

                insert_logging(
                    summary='Webhook - Success sending to AMQP server',
                    description='Its wating for next step in the process chain to be processed to the right Docker Swarm Clusters',
                    binds=[
                        f'webook_id-{str(webhook_data.pk)}',
                        f'webook_number-{webhook_data.number}',
                        f'webook_identifier-{webhook_data.identifier}',
                    ]
                )

            except Exception:
                insert_logging(
                    summary='Webhook - Failed to sending it to AMQP server',
                    level='error',
                    binds=[
                        f'webook_id-{str(webhook_data.pk)}',
                        f'webook_number-{webhook_data.number}',
                        f'webook_identifier-{webhook_data.identifier}',
                    ]
                )
        else:
            insert_logging(
                summary='Webhook - AMQP process is disabled',
                description='Its mean the system will not automatic deploy this webhook out.',
                binds=[
                    f'webook_id-{str(webhook_data.pk)}',
                    f'webook_number-{webhook_data.number}',
                    f'webook_identifier-{webhook_data.identifier}',
                ]
            )
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

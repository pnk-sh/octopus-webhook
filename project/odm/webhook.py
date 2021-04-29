from bson.json_util import default
from mongoengine import Document
from mongoengine.fields import DictField, SequenceField, StringField

WEBHOOK_STATUS = ("pending",)


class Webhook(Document):
    number = SequenceField()
    status = StringField(choices=WEBHOOK_STATUS, default="pending")
    identifier = StringField()
    webhook = DictField()

    meta = {"indexes": [{"fields": ["identifier"]}, {"fields": ["status"]}]}

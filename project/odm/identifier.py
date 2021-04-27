from enum import unique
from bson.json_util import default
from mongoengine import Document
from mongoengine.fields import StringField

class Identifier(Document):
    name = StringField()
    key = StringField(unique=True)

    meta = {
    }

from mongoengine import Document
from mongoengine.fields import StringField

class Identifier(Document):
    name = StringField()
    key = StringField(unique=True)

    meta = {
    }

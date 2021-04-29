from bson.json_util import dumps, loads
from flask import Response, request

from project.odm.identifier import Identifier as OdmIdentifier


class Identifiers:
    @staticmethod
    def get_all():
        identifier = OdmIdentifier.objects()

        return (
            Response(
                dumps({"status": 200, "content": loads(identifier.to_json())}),
                mimetype="text/json",
            ),
            200,
        )

    @staticmethod
    def create():
        data = request.get_json()

        identifier = OdmIdentifier()
        identifier.name = data.get("name")
        identifier.key = data.get("key")
        identifier.save()

        return (
            Response(
                dumps({"status": 200, "content": {"pk": identifier.pk}}),
                mimetype="text/json",
            ),
            200,
        )

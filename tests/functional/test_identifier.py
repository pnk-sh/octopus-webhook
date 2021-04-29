from base64 import b64encode
from bson.json_util import dumps, loads

from project.flask import create_app
from project.odm.identifier import Identifier as OdmIdentifier


def test_identifier_get_all():
    OdmIdentifier.drop_collection()

    identifier = OdmIdentifier()
    identifier.name = "Test Hook 1"
    identifier.key = "test-hook-1"
    identifier.save()

    identifier = OdmIdentifier()
    identifier.name = "Test Hook 2"
    identifier.key = "test-hook-2"
    identifier.save()

    identifier = OdmIdentifier()
    identifier.name = "Test Hook 3"
    identifier.key = "test-hook-3"
    identifier.save()

    app = create_app()

    credentials = b64encode(b"admin:secret").decode("utf-8")
    response = app.test_client().get(
        "/identifier", headers={"Authorization": "Basic {}".format(credentials)}
    )
    assert response.status_code == 200

    json_data = loads(response.get_data(as_text=True))
    assert len(json_data["content"]) == 3


def test_identifier_create():
    OdmIdentifier.drop_collection()

    app = create_app()

    assert True

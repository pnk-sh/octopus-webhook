from project.flask import create_app
from project.odm.identifier import Identifier as OdmIdentifier


def test_identifier_create():
    OdmIdentifier.drop_collection()

    app = create_app()

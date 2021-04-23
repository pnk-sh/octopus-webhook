import os
import logging
from werkzeug.wrappers import Request, Response
from odm.identifier import Identifier

class AuthNotAllowed(Exception):
    pass

class AuthIdentifier:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        try:
            
            args_identifier = request.args.get('identifier')

            try:
                identifier_data = Identifier.objects.get(key=args_identifier)
            except Exception:
                raise AuthNotAllowed()

            logging.info('Auth Identifier success')
            return self.app(environ, start_response)

        except AuthNotAllowed as e:
            logging.info('Auth Identifier failed')

            res = Response(u'Auth Identifier failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
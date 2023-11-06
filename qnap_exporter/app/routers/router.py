from flask import request, current_app as app
from ..database import get_db
from ..utils import normalize_name


log = app.logger


DEFAULT_SERVICE = 'service'
# FIXME: replace with a constant
DEFAULT_SERVER = 'qnap_exporter'


class RouterException(Exception):
    pass


class Router(object):
    def __init__(self, database=None):
        if not database:
            database = get_db()
        self.db = database

    @property
    def service(self):
        return DEFAULT_SERVICE

    @property
    def server(self):
        return DEFAULT_SERVER

    def get_request_json(self):
        return request.json

    def base_response(self, action):
        action = normalize_name(action)
        return dict({
            'server': self.server,
            'service': self.service,
            'action': action,
            'message': 'finished',
        })

from flask import current_app as app
from qnapstats import QNAPStats


log = app.logger


class QNAPClientException(Exception):
    pass


class QNAPClient(object):
    # @classmethod
    # def get_client(cls):
    #     return cls()

    def __init__(self, host, port, username, password, verify_ssl=False):
        self.client = QNAPStats(host, port, username, password, verify_ssl=verify_ssl)

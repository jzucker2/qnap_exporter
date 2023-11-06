from flask import current_app as app
from ..common.domains import Domains
from .qnap_client import QNAPClient


log = app.logger


class ExporterException(Exception):
    pass


class Exporter(object):
    DEFAULT_SYSTEM_HEALTH_VALUE = 'missing'

    @classmethod
    def get_client(cls, qnap_client=None):
        if not qnap_client:
            qnap_client = QNAPClient.get_client()
        return cls(qnap_client)

    def __init__(self, qnap_client):
        self.qnap_client = qnap_client
        self._domains = {
            Domains.SYSTEM_STATS: {},
            Domains.BANDWIDTH: {},
            Domains.VOLUMES: {},
            Domains.SMART_DISK_HEALTH: {},
            Domains.SYSTEM_HEALTH: self.DEFAULT_SYSTEM_HEALTH_VALUE,
        }

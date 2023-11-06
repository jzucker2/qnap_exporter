from flask import current_app as app
from qnapstats import QNAPStats


log = app.logger


QNAP_HOST_IP = app.config.get('QNAP_HOST_IP')
QNAP_PORT = app.config.get('QNAP_PORT')
QNAP_USERNAME = app.config.get('QNAP_USERNAME')
QNAP_PASSWORD = app.config.get('QNAP_PASSWORD')


class QNAPClientException(Exception):
    pass


class QNAPClient(object):
    @classmethod
    def get_client(cls):
        host = QNAP_HOST_IP
        port = QNAP_PORT
        username = QNAP_USERNAME
        password = QNAP_PASSWORD
        return cls(host, port, username, password)

    def __init__(self, host, port, username, password, verify_ssl=False):
        self.client = QNAPStats(host, port, username, password, verify_ssl=verify_ssl)

    def get_system_health(self):
        return self.client.get_system_health()

    def get_volumes(self):
        return self.client.get_volumes()

    def get_bandwidth(self):
        return self.client.get_bandwidth()

    def get_system_stats(self):
        return self.client.get_system_stats()

    def get_smart_disk_health(self):
        return self.client.get_smart_disk_health()

    def get_firmware_update(self):
        return self.client.get_firmware_update()

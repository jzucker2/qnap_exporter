from requests.exceptions import RequestException
from flask import current_app as app
from qnapstats import QNAPStats


log = app.logger


QNAP_NAS_NAME = app.config.get('QNAP_NAS_NAME')
QNAP_HOST_IP = app.config.get('QNAP_HOST_IP')
QNAP_PORT = app.config.get('QNAP_PORT')
QNAP_USERNAME = app.config.get('QNAP_USERNAME')
QNAP_PASSWORD = app.config.get('QNAP_PASSWORD')


class QNAPClientException(Exception):
    pass


class QNAPClientRequestException(QNAPClientException):
    pass


class QNAPClient(object):
    @classmethod
    def get_default_client(cls):
        nas_name = QNAP_NAS_NAME
        host = QNAP_HOST_IP
        port = QNAP_PORT
        username = QNAP_USERNAME
        password = QNAP_PASSWORD
        return cls(host, port, username, password, nas_name=nas_name)

    @classmethod
    def get_collecting_client(cls, nas_name, host, port, username, password):
        return cls(host, port, username, password, nas_name=nas_name)

    def __init__(self,
                 host,
                 port,
                 username,
                 password,
                 nas_name=None,
                 verify_ssl=False):
        super().__init__()
        if not nas_name:
            nas_name = QNAP_NAS_NAME
        self._nas_name = nas_name
        self.client = QNAPStats(
            host,
            port,
            username,
            password,
            verify_ssl=verify_ssl)

    @property
    def nas_name(self):
        return self._nas_name

    def get_system_health(self):
        try:
            return self.client.get_system_health()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_volumes(self):
        log.debug(f'self.nas_name: {self.nas_name} get_volumes')
        try:
            return self.client.get_volumes()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_bandwidth(self):
        try:
            return self.client.get_bandwidth()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_system_stats(self):
        try:
            return self.client.get_system_stats()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_smart_disk_health(self):
        try:
            return self.client.get_smart_disk_health()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_firmware_update(self):
        try:
            return self.client.get_firmware_update()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

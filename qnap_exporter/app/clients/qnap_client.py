from requests.exceptions import RequestException
from flask import current_app as app
from qnapstats import QNAPStats


log = app.logger


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
    def get_client(cls):
        host = QNAP_HOST_IP
        port = QNAP_PORT
        username = QNAP_USERNAME
        password = QNAP_PASSWORD
        return cls(host, port, username, password)

    def __init__(self, host, port, username, password, verify_ssl=False):
        super().__init__()
        self.client = QNAPStats(
            host,
            port,
            username,
            password,
            verify_ssl=verify_ssl)

    def get_system_health(self):
        try:
            return self.client.get_system_health()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def get_volumes(self):
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

    def safe_get_debug_firmware_update(self):
        try:
            return self._get_debug_firmware_update()
        except RequestException as re:
            r_m = f'request got re: {re}'
            raise QNAPClientRequestException(r_m)

    def _get_debug_firmware_update(self):
        """Get firmware update version if available."""
        resp = self.client._get_url("sys/sysRequest.cgi?subfunc=firm_update")
        if resp is None:
            return None

        d_m = f'debug_firmware_update got resp: {resp}'
        log.info(d_m)

        new_version = resp["func"]["ownContent"]["newVersion"]
        if new_version is None or len(new_version) == 0:
            return None

        return new_version

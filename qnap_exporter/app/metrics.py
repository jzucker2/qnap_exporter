from enum import Enum
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from prometheus_flask_exporter import Counter, Summary


class Labels(Enum):
    DEVICE = 'device'

    @classmethod
    def labels(cls):
        return list([
            cls.DEVICE.value,
        ])


class Metrics(object):
    SEND_MAGIC_PACKET_TIME = Summary(
        'qnap_exporter_wal_send_magic_pack_time',
        'Time spent to send WAL magic packet')

    SEND_MAGIC_PACKET_EXCEPTIONS = Counter(
        'qnap_exporter_wal_send_magic_pack_exceptions',
        'Exceptions while attempting to send WAL magic packet')

    DEBUG_ROUTE_TIME = Summary(
        'qnap_exporter_debug_route_time',
        'Time spent to handle debug route request')

    DEBUG_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_debug_route_exceptions',
        'Exceptions while attempting to handle debug route request')


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

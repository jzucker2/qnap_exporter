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
    DEBUG_ROUTE_TIME = Summary(
        'qnap_exporter_debug_route_time',
        'Time spent to handle debug route request')

    DEBUG_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_debug_route_exceptions',
        'Exceptions while attempting to handle debug route request')

    SIMPLE_EXPORTER_ROUTE_TIME = Summary(
        'qnap_exporter_simple_exporter_route_time',
        'Time spent to handle simple exporter route request')

    SIMPLE_EXPORTER_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_simple_exporter_route_exceptions',
        'Exceptions while attempting to handle simple exporter route request')


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

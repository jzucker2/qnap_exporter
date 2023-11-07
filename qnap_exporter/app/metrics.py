from enum import Enum
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from prometheus_flask_exporter import Counter, Summary, Gauge


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

    EXPORTER_METRICS_UPDATE_ROUTE_TIME = Summary(
        'qnap_exporter_exporter_metrics_update_route_time',
        'Time spent to handle exporter metrics update route request')

    EXPORTER_METRICS_UPDATE_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_exporter_metrics_update_route_exceptions',
        'Exceptions while attempting exporter metrics update route request')

    SYSTEM_STATS_CPU_TEMP_C_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_temp_c',
        'Current temp of CPU in Celsius')

    SYSTEM_STATS_CPU_TEMP_F_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_temp_f',
        'Current temp of CPU in Fahrenheit')

    SYSTEM_STATS_CPU_USAGE_PERCENT_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_usage_percent',
        'Current system CPU usage percentage')

    SYSTEM_STATS_MEMORY_FREE_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_free',
        'Current free system memory of the QNAP')

    SYSTEM_STATS_MEMORY_TOTAL_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_total',
        'The total system memory of the QNAP')


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

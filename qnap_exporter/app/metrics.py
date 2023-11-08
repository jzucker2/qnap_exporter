from enum import Enum
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from prometheus_flask_exporter import Counter, Summary, Gauge


class Labels(Enum):
    DEVICE = 'device'
    NETWORK_ID = 'network_id'
    NETWORK_NAME = 'network_name'
    IS_DEFAULT = 'is_default'
    IP = 'ip'
    MAC = 'mac'
    MASK = 'mask'
    USAGE = 'usage'
    VOLUME_ID = 'volume_id'
    VOLUME_ID_NUMBER = 'volume_id_number'
    VOLUME_LABEL = 'volume_label'
    MODEL = 'model'
    DISK_ID = 'disk_id'
    DISK_TYPE = 'disk_type'
    DRIVE_NUMBER = 'drive_number'

    @classmethod
    def labels(cls):
        return list([
            cls.DEVICE.value,
        ])

    @classmethod
    def bandwidth_labels(cls):
        return list([
            cls.NETWORK_ID.value,
            cls.NETWORK_NAME.value,
            cls.IS_DEFAULT.value,
        ])

    @classmethod
    def nics_labels(cls):
        return list([
            cls.NETWORK_ID.value,
            cls.IP.value,
            cls.MAC.value,
            cls.USAGE.value,
        ])

    @classmethod
    def volume_labels(cls):
        return list([
            cls.VOLUME_ID.value,
            cls.VOLUME_ID_NUMBER.value,
            cls.VOLUME_LABEL.value,
        ])

    @classmethod
    def smart_disk_labels(cls):
        return list([
            cls.DISK_ID.value,
            cls.DRIVE_NUMBER.value,
            cls.MODEL.value,
            cls.DISK_TYPE.value,
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

    SYSTEM_STATS_UPTIME_SECONDS = Gauge(
        'qnap_exporter_system_stats_uptime_seconds',
        'The total system uptime of the QNAP in seconds')

    SYSTEM_STATS_NICS_RX_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_rx_packets',
        'The QNAP system stats nics rx_packets',
        Labels.nics_labels())

    SYSTEM_STATS_NICS_TX_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_tx_packets',
        'The QNAP system stats nics tx_packets',
        Labels.nics_labels())

    SYSTEM_STATS_NICS_ERR_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_err_packets',
        'The QNAP system stats nics err_packets',
        Labels.nics_labels())

    SYSTEM_STATS_NICS_MAX_SPEED = Gauge(
        'qnap_exporter_system_stats_nics_max_speed',
        'The QNAP system stats nics max speed',
        Labels.nics_labels())

    BANDWIDTH_INTERFACE_RX = Gauge(
        'qnap_exporter_bandwidth_interface_rx',
        'The QNAP bandwidth network interface rx value',
        Labels.bandwidth_labels())

    BANDWIDTH_INTERFACE_TX = Gauge(
        'qnap_exporter_bandwidth_interface_tx',
        'The QNAP bandwidth network interface tx value',
        Labels.bandwidth_labels())

    VOLUME_FREE_SIZE = Gauge(
        'qnap_exporter_volume_free_size',
        'The QNAP volume free size (bytes?)',
        Labels.volume_labels())

    VOLUME_TOTAL_SIZE = Gauge(
        'qnap_exporter_volume_total_size',
        'The QNAP volume total size (bytes?)',
        Labels.volume_labels())

    SMART_DISK_HEALTH_TEMP_C_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_temp_c',
        'Current temp of disk in Celsius',
        Labels.smart_disk_labels())

    SMART_DISK_HEALTH_TEMP_F_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_temp_f',
        'Current temp of disk in Fahrenheit',
        Labels.smart_disk_labels())


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

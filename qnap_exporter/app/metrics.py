from enum import Enum
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from prometheus_flask_exporter import Counter, Summary, Gauge


class Labels(Enum):
    NAS_NAME = 'nas_name'
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
    SHARENAME = 'sharename'
    MODEL = 'model'
    DISK_ID = 'disk_id'
    DISK_TYPE = 'disk_type'
    DRIVE_NUMBER = 'drive_number'
    SERIAL = 'serial'
    UNITS = 'units'

    @classmethod
    def labels(cls):
        return list([
            cls.DEVICE.value,
        ])

    @classmethod
    def nas_name_labels(cls):
        return list([
            cls.NAS_NAME.value,
        ])

    @classmethod
    def bandwidth_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.NETWORK_ID.value,
            cls.NETWORK_NAME.value,
            cls.IS_DEFAULT.value,
        ])

    @classmethod
    def nics_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.NETWORK_ID.value,
            cls.IP.value,
            cls.MAC.value,
            cls.USAGE.value,
        ])

    @classmethod
    def volume_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.VOLUME_ID.value,
            cls.VOLUME_ID_NUMBER.value,
            cls.VOLUME_LABEL.value,
        ])

    @classmethod
    def volume_folder_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.VOLUME_ID.value,
            cls.VOLUME_ID_NUMBER.value,
            cls.VOLUME_LABEL.value,
            cls.SHARENAME.value,
        ])

    @classmethod
    def smart_disk_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.DISK_ID.value,
            cls.DRIVE_NUMBER.value,
            cls.MODEL.value,
            cls.SERIAL.value,
            cls.DISK_TYPE.value,
        ])

    @classmethod
    def smart_disk_capacity_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.DISK_ID.value,
            cls.DRIVE_NUMBER.value,
            cls.MODEL.value,
            cls.SERIAL.value,
            cls.DISK_TYPE.value,
            cls.UNITS.value,
        ])

    @classmethod
    def default_system_stats_labels(cls):
        return list(cls.nas_name_labels())


class Metrics(object):
    # This is just for simple debug stuff
    DEBUG_ROUTE_TIME = Summary(
        'qnap_exporter_debug_route_time',
        'Time spent to handle debug route request')

    DEBUG_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_debug_route_exceptions',
        'Exceptions while attempting to handle debug route request')

    # For collector process that scrapes info from QNAP devices

    SIMPLE_COLLECTOR_ROUTE_TIME = Summary(
        'qnap_exporter_simple_collector_route_time',
        'Time spent to handle simple collector route request',
        Labels.nas_name_labels())

    SIMPLE_COLLECTOR_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_simple_collector_route_exceptions',
        'Exceptions while attempting to handle simple collector route request',
        Labels.nas_name_labels())

    COLLECTOR_METRICS_UPDATE_ROUTE_TIME = Summary(
        'qnap_exporter_collector_metrics_update_route_time',
        'Time spent to handle collector metrics update route request',
        Labels.nas_name_labels())

    COLLECTOR_METRICS_UPDATE_ROUTE_EXCEPTIONS = Counter(
        'qnap_exporter_collector_metrics_update_route_exceptions',
        'Exceptions while attempting collector metrics update route request',
        Labels.nas_name_labels())

    # Below are for actual QNAP NAS instances

    SYSTEM_STATS_CPU_TEMP_C_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_temp_c',
        'Current temp of CPU in Celsius',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_CPU_TEMP_F_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_temp_f',
        'Current temp of CPU in Fahrenheit',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_SYSTEM_TEMP_C_VALUE = Gauge(
        'qnap_exporter_system_stats_system_temp_c',
        'Current temp of entire QNAP system in Celsius',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_SYSTEM_TEMP_F_VALUE = Gauge(
        'qnap_exporter_system_stats_system_temp_f',
        'Current temp of entire QNAP system in Fahrenheit',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_CPU_USAGE_PERCENT_VALUE = Gauge(
        'qnap_exporter_system_stats_cpu_usage_percent',
        'Current system CPU usage percentage',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_MEMORY_FREE_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_free',
        'Current free system memory of the QNAP',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_MEMORY_TOTAL_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_total',
        'The total system memory of the QNAP',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_MEMORY_USED_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_used',
        'The used system memory of the QNAP',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_MEMORY_USAGE_PERCENT = Gauge(
        'qnap_exporter_system_stats_memory_usage_percent',
        'The % of system memory currently being used of the QNAP',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_UPTIME_SECONDS = Gauge(
        'qnap_exporter_system_stats_uptime_seconds',
        'The total system uptime of the QNAP in seconds',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_NICS_RX_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_rx_packets_total',
        'The QNAP system stats nics rx_packets',
        Labels.nics_labels())

    SYSTEM_STATS_NICS_TX_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_tx_packets_total',
        'The QNAP system stats nics tx_packets',
        Labels.nics_labels())

    SYSTEM_STATS_NICS_ERR_PACKETS = Gauge(
        'qnap_exporter_system_stats_nics_err_packets_total',
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

    VOLUME_USED_SIZE = Gauge(
        'qnap_exporter_volume_used_size',
        'The QNAP volume used size (bytes?)',
        Labels.volume_labels())

    VOLUME_USAGE_PERCENT = Gauge(
        'qnap_exporter_volume_usage_percent',
        'The QNAP volume usage %',
        Labels.volume_labels())

    VOLUME_FOLDER_USED_SIZE = Gauge(
        'qnap_exporter_volume_folder_used_size',
        'The QNAP volume folder used size (bytes?)',
        Labels.volume_folder_labels())

    SMART_DISK_HEALTH_TEMP_C_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_temp_c',
        'Current temp of disk in Celsius',
        Labels.smart_disk_labels())

    SMART_DISK_HEALTH_TEMP_F_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_temp_f',
        'Current temp of disk in Fahrenheit',
        Labels.smart_disk_labels())

    SMART_DISK_HEALTH_CAPACITY_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_capacity',
        'Current capacity of disk in dynamically labelled units',
        Labels.smart_disk_capacity_labels())


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

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
    VERSION = 'version'
    BUILD = 'build'
    PATCH = 'patch'
    BUILD_TIME = 'build_time'
    SYSTEM_HEALTH_STATUS = 'system_health_status'
    CPU_MODEL = 'cpu_model'
    DISK_HEALTH = 'disk_health'
    SYSTEM_MODEL = 'system_model'
    SYSTEM_NAME = 'system_name'
    SYSTEM_SERIAL_NUMBER = 'system_serial_number'
    SYSTEM_TIMEZONE = 'system_timezone'
    DNS = 'dns'
    MEMORY_TYPE = 'memory_type'
    LINK_STATUS = 'link_status'
    TRANSFER_TYPE = 'transfer_type'

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
    def system_health_status_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.SYSTEM_HEALTH_STATUS.value,
        ])

    @classmethod
    def bandwidth_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.NETWORK_ID.value,
            cls.NETWORK_NAME.value,
            cls.IS_DEFAULT.value,
            cls.TRANSFER_TYPE.value,
        ])

    @classmethod
    def nics_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.NETWORK_ID.value,
            cls.IP.value,
            cls.MAC.value,
            cls.USAGE.value,
            cls.LINK_STATUS.value,
            cls.MASK.value,
        ])

    @classmethod
    def nics_packet_labels(cls):
        final_packet_labels = cls.nics_labels()
        final_packet_labels.extend([
            cls.TRANSFER_TYPE.value,
        ])
        return list(final_packet_labels)

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
            cls.DISK_HEALTH.value,
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
            cls.DISK_HEALTH.value,
        ])

    @classmethod
    def firmware_info_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.VERSION.value,
            cls.BUILD.value,
            cls.PATCH.value,
            cls.BUILD_TIME.value,
        ])

    @classmethod
    def cpu_info_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.CPU_MODEL.value,
        ])

    @classmethod
    def system_info_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.SYSTEM_NAME.value,
            cls.SYSTEM_MODEL.value,
            cls.SYSTEM_SERIAL_NUMBER.value,
            cls.SYSTEM_TIMEZONE.value,
        ])

    @classmethod
    def dns_info_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.DNS.value,
        ])

    @classmethod
    def default_system_stats_labels(cls):
        return list(cls.nas_name_labels())

    @classmethod
    def memory_stats_labels(cls):
        return list([
            cls.NAS_NAME.value,
            cls.MEMORY_TYPE.value,
        ])


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
    # for units, see https://github.com/home-assistant/core/blob/dev/homeassistant/components/qnap/sensor.py  # noqa: E501

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

    SYSTEM_STATS_MEMORY_TYPE_VALUE = Gauge(
        'qnap_exporter_system_stats_memory_type_total',
        'Current system memory for memory_type of the QNAP',
        Labels.memory_stats_labels())

    SYSTEM_STATS_MEMORY_USAGE_PERCENT = Gauge(
        'qnap_exporter_system_stats_memory_usage_percent',
        'The % of system memory currently being used of the QNAP',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_UPTIME_SECONDS = Gauge(
        'qnap_exporter_system_stats_uptime_seconds',
        'The total system uptime of the QNAP in seconds',
        Labels.default_system_stats_labels())

    SYSTEM_STATS_NICS_PACKETS_TOTAL = Gauge(
        'qnap_exporter_system_stats_nics_packets_total',
        'The QNAP system stats nics packets by type',
        Labels.nics_packet_labels())

    SYSTEM_STATS_NICS_MAX_SPEED = Gauge(
        'qnap_exporter_system_stats_nics_max_speed_total',
        'The QNAP system stats nics max speed',
        Labels.nics_labels())

    BANDWIDTH_INTERFACE_TRANSFER_RATE = Gauge(
        'qnap_exporter_bandwidth_interface_transfer_rate',
        'The QNAP bandwidth network interface transfer rate value',
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

    SMART_DISK_HEALTH_CAPACITY_NORMALIZED_VALUE = Gauge(
        'qnap_exporter_smart_disk_health_capacity_normalized',
        'Current capacity (normalized to MB) of disk in labelled units',
        Labels.smart_disk_capacity_labels())

    NAS_FIRMWARE_INFO = Gauge(
        'qnap_exporter_nas_firmware_info',
        'Info dict for the firmware of the NAS',
        Labels.firmware_info_labels())

    NAS_SYSTEM_INFO = Gauge(
        'qnap_exporter_nas_system_info',
        'Info dict for the system of the NAS',
        Labels.system_info_labels())

    NAS_CPU_INFO = Gauge(
        'qnap_exporter_nas_cpu_info',
        'Info dict for the CPU of the NAS',
        Labels.cpu_info_labels())

    NAS_DNS_INFO = Gauge(
        'qnap_exporter_nas_dns_info',
        'Info dict for the DNS of the NAS',
        Labels.dns_info_labels())

    SYSTEM_HEALTH_STATUS = Gauge(
        'qnap_exporter_nas_system_health_status',
        'The latest system health status reported by the NAS',
        Labels.system_health_status_labels())


# https://github.com/rycus86/prometheus_flask_exporter#app-factory-pattern
# https://github.com/rycus86/prometheus_flask_exporter/blob/master/examples/gunicorn-app-factory/app_setup.py
def get_metrics_app_factory():
    return GunicornPrometheusMetrics.for_app_factory()


metrics = get_metrics_app_factory()

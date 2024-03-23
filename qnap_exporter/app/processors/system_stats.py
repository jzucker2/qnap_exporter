from datetime import timedelta
from flask import current_app as app
from ..metrics import Metrics
from ..common.memory_types import MemoryTypes
from ..common.bandwidth_transfer_types import BandwidthTransferTypes
from ..common.system_stats_keys import SystemStatsKeys
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class UptimeDictKeys(object):
    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'


class NICSInterfaceDictKeys(object):
    ERR_PACKETS = 'err_packets'
    IP = 'ip'
    LINK_STATUS = 'link_status'
    MAC = 'mac'
    MASK = 'mask'
    MAX_SPEED = 'max_speed'
    RX_PACKETS = 'rx_packets'
    TX_PACKETS = 'tx_packets'
    USAGE = 'usage'


class CPUDictKeys(object):
    MODEL = 'model'
    TEMP_C = 'temp_c'
    TEMP_F = 'temp_f'
    USAGE_PERCENT = 'usage_percent'


class MemoryDictKeys(object):
    FREE = 'free'
    TOTAL = 'total'


class SystemDictKeys(object):
    MODEL = 'model'
    NAME = 'name'
    SERIAL_NUMBER = 'serial_number'
    TEMP_C = 'temp_c'
    TEMP_F = 'temp_f'
    TIMEZONE = 'timezone'


class FirmwareDictKeys(object):
    VERSION = 'version'
    BUILD = 'build'
    PATCH = 'patch'
    BUILD_TIME = 'build_time'


class SystemStatsProcessorException(BaseProcessorException):
    pass


class InvalidFirmwarePropertyProcessorException(SystemStatsProcessorException):
    pass


class InvalidSysTransferTypeProcessorException(SystemStatsProcessorException):
    pass


class SystemStatsProcessor(BaseProcessor):
    def _convert_uptime_dict(self, uptime_dict):
        log.debug(f'starting with uptime_dict: {uptime_dict}')
        days = uptime_dict[UptimeDictKeys.DAYS]
        hours = uptime_dict[UptimeDictKeys.HOURS]
        minutes = uptime_dict[UptimeDictKeys.MINUTES]
        seconds = uptime_dict[UptimeDictKeys.SECONDS]
        uptime_delta = timedelta(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds)
        total_seconds = uptime_delta.total_seconds()
        f_m = (f'converted uptime_dict: {uptime_dict} '
               f'to uptime_delta: {uptime_delta} with '
               f'total_seconds: {total_seconds}')
        log.debug(f_m)
        return total_seconds

    def _handle_system_dict(self, stats):
        system = stats.get(SystemStatsKeys.SYSTEM)
        log.debug(f'system: {system}')
        model = system.get(SystemDictKeys.MODEL)
        name = system.get(SystemDictKeys.NAME)
        timezone = system.get(SystemDictKeys.TIMEZONE)
        serial = system.get(SystemDictKeys.SERIAL_NUMBER)
        i_m = (f'system info model: {model}, name: {name}, '
               f'timezone: {timezone}, serial: {serial}')
        log.debug(i_m)
        Metrics.NAS_SYSTEM_INFO.labels(
            nas_name=self.nas_name,
            system_name=name,
            system_model=model,
            system_serial_number=serial,
            system_timezone=timezone,
        ).set(1)
        temp_c = system.get(SystemDictKeys.TEMP_C)
        temp_f = system.get(SystemDictKeys.TEMP_F)
        Metrics.SYSTEM_STATS_SYSTEM_TEMP_C_VALUE.labels(
            nas_name=self.nas_name,
        ).set(temp_c)
        Metrics.SYSTEM_STATS_SYSTEM_TEMP_F_VALUE.labels(
            nas_name=self.nas_name,
        ).set(temp_f)

    def _handle_uptime_dict(self, stats):
        uptime = stats.get(SystemStatsKeys.UPTIME)
        log.debug(f'uptime: {uptime}')
        uptime_seconds = self._convert_uptime_dict(uptime)
        Metrics.SYSTEM_STATS_UPTIME_SECONDS.labels(
            nas_name=self.nas_name,
        ).set(uptime_seconds)

    def _handle_memory_dict(self, stats):
        memory = stats.get(SystemStatsKeys.MEMORY)
        if not memory:
            return
        free = memory.get(MemoryDictKeys.FREE, 0)
        Metrics.SYSTEM_STATS_MEMORY_TYPE_VALUE.labels(
            nas_name=self.nas_name,
            memory_type=MemoryTypes.FREE.value,
        ).set(free)
        total = memory.get(MemoryDictKeys.TOTAL, 0)
        Metrics.SYSTEM_STATS_MEMORY_TYPE_VALUE.labels(
            nas_name=self.nas_name,
            memory_type=MemoryTypes.TOTAL.value,
        ).set(total)
        log.debug(f'memory stats => {free}/{total}')
        used = total - free
        Metrics.SYSTEM_STATS_MEMORY_TYPE_VALUE.labels(
            nas_name=self.nas_name,
            memory_type=MemoryTypes.USED.value,
        ).set(used)
        usage = (used / total) * 100
        u_m = f'_handle_memory_dict got usage: {usage} from ({used}/{total})'
        log.debug(u_m)
        Metrics.SYSTEM_STATS_MEMORY_USAGE_PERCENT.labels(
            nas_name=self.nas_name,
        ).set(usage)

    def _handle_cpu_dict(self, stats):
        cpu = stats.get(SystemStatsKeys.CPU)
        if not cpu:
            return
        cpu_model = cpu.get(CPUDictKeys.MODEL)
        log.debug(f'cpu_model: {cpu_model}')
        Metrics.NAS_CPU_INFO.labels(
            nas_name=self.nas_name,
            cpu_model=cpu_model,
        ).set(1)
        temp_c = cpu.get(CPUDictKeys.TEMP_C, 0)
        Metrics.SYSTEM_STATS_CPU_TEMP_C_VALUE.labels(
            nas_name=self.nas_name,
        ).set(temp_c)
        temp_f = cpu.get(CPUDictKeys.TEMP_F, 0)
        Metrics.SYSTEM_STATS_CPU_TEMP_F_VALUE.labels(
            nas_name=self.nas_name,
        ).set(temp_f)
        usage_percent = cpu.get(CPUDictKeys.USAGE_PERCENT, 0)
        Metrics.SYSTEM_STATS_CPU_USAGE_PERCENT_VALUE.labels(
            nas_name=self.nas_name,
        ).set(usage_percent)
        log.debug(f'cpu stats => {temp_c}, {temp_f}, {usage_percent}')

    def _get_packet_count(self, transfer_type, network_stats):
        packet_key = None
        if transfer_type == BandwidthTransferTypes.TX:
            packet_key = NICSInterfaceDictKeys.TX_PACKETS
        elif transfer_type == BandwidthTransferTypes.RX:
            packet_key = NICSInterfaceDictKeys.RX_PACKETS
        elif transfer_type == BandwidthTransferTypes.ERR:
            packet_key = NICSInterfaceDictKeys.ERR_PACKETS
        else:
            e_m = f'Invalid transfer_type: {transfer_type}'
            log.error(e_m)
            raise InvalidSysTransferTypeProcessorException(e_m)
        final_packet_count = network_stats.get(packet_key, 0)
        t_m = (f'transfer_type: {transfer_type} got '
               f'final_packet_count: {final_packet_count}')
        log.debug(t_m)
        return final_packet_count

    def _handle_nics_interface(self, network_id, network_stats):
        ip = network_stats.get(NICSInterfaceDictKeys.IP)
        mac = network_stats.get(NICSInterfaceDictKeys.MAC)
        usage = network_stats.get(NICSInterfaceDictKeys.USAGE)
        link_status = network_stats.get(NICSInterfaceDictKeys.LINK_STATUS)
        mask = network_stats.get(NICSInterfaceDictKeys.MASK)
        max_speed = network_stats.get(NICSInterfaceDictKeys.MAX_SPEED)
        Metrics.SYSTEM_STATS_NICS_MAX_SPEED.labels(
            nas_name=self.nas_name,
            network_id=network_id,
            ip=ip,
            mac=mac,
            usage=usage,
            link_status=link_status,
            mask=mask,
        ).set(max_speed)
        for transfer_type in BandwidthTransferTypes.nics_packet_metrics_list():
            packet_count = self._get_packet_count(transfer_type, network_stats)
            Metrics.SYSTEM_STATS_NICS_PACKETS_TOTAL.labels(
                nas_name=self.nas_name,
                network_id=network_id,
                ip=ip,
                mac=mac,
                usage=usage,
                link_status=link_status,
                mask=mask,
                transfer_type=transfer_type.label_string,
            ).set(packet_count)

    def _handle_nics_dict(self, stats):
        nics = stats.get(SystemStatsKeys.NICS)
        if not nics:
            return
        for key, value in nics.items():
            self._handle_nics_interface(key, value)

    def _handle_firmware_dict(self, stats):
        firmware = stats.get(SystemStatsKeys.FIRMWARE)
        if not firmware:
            return
        log.debug(f'got firmware: {firmware}')
        labels = {
            'nas_name': self.nas_name,
        }
        labels.update({k: str(v) for k, v in firmware.items()})
        Metrics.NAS_FIRMWARE_INFO.labels(**labels).set(1)

    def _handle_dns_dict(self, stats):
        dns = stats.get(SystemStatsKeys.DNS)
        if not dns:
            return
        log.debug(f'got dns: {dns}')
        for dns_value in dns:
            Metrics.NAS_DNS_INFO.labels(
                nas_name=self.nas_name,
                dns=dns_value,
            ).set(1)

    def process(self, stats, last_updated=None):
        m = (f'_process_system_stats => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return
        self._handle_cpu_dict(stats)
        self._handle_memory_dict(stats)
        self._handle_uptime_dict(stats)
        self._handle_nics_dict(stats)
        self._handle_firmware_dict(stats)
        self._handle_system_dict(stats)
        self._handle_dns_dict(stats)

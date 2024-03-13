from datetime import timedelta
from flask import current_app as app
from ..metrics import Metrics
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


class SystemStatsProcessorException(BaseProcessorException):
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
        temp_c = system.get(SystemDictKeys.TEMP_C)
        temp_f = system.get(SystemDictKeys.TEMP_F)
        Metrics.SYSTEM_STATS_SYSTEM_TEMP_C_VALUE.set(temp_c)
        Metrics.SYSTEM_STATS_SYSTEM_TEMP_F_VALUE.set(temp_f)

    def _handle_uptime_dict(self, stats):
        uptime = stats.get(SystemStatsKeys.UPTIME)
        log.debug(f'uptime: {uptime}')
        uptime_seconds = self._convert_uptime_dict(uptime)
        Metrics.SYSTEM_STATS_UPTIME_SECONDS.set(uptime_seconds)

    def _handle_memory_dict(self, stats):
        memory = stats.get(SystemStatsKeys.MEMORY)
        if not memory:
            return
        free = memory.get(MemoryDictKeys.FREE, 0)
        Metrics.SYSTEM_STATS_MEMORY_FREE_VALUE.set(free)
        total = memory.get(MemoryDictKeys.TOTAL, 0)
        Metrics.SYSTEM_STATS_MEMORY_TOTAL_VALUE.set(total)
        log.debug(f'memory stats => {free}/{total}')
        used = total - free
        Metrics.SYSTEM_STATS_MEMORY_USED_VALUE.set(used)
        usage = (used / total) * 100
        u_m = f'_handle_memory_dict got usage: {usage} from ({used}/{total})'
        log.debug(u_m)
        Metrics.SYSTEM_STATS_MEMORY_USAGE_PERCENT.set(usage)

    def _handle_cpu_dict(self, stats):
        cpu = stats.get(SystemStatsKeys.CPU)
        if not cpu:
            return
        temp_c = cpu.get(CPUDictKeys.TEMP_C, 0)
        Metrics.SYSTEM_STATS_CPU_TEMP_C_VALUE.set(temp_c)
        temp_f = cpu.get(CPUDictKeys.TEMP_F, 0)
        Metrics.SYSTEM_STATS_CPU_TEMP_F_VALUE.set(temp_f)
        usage_percent = cpu.get(CPUDictKeys.USAGE_PERCENT, 0)
        Metrics.SYSTEM_STATS_CPU_USAGE_PERCENT_VALUE.set(usage_percent)
        log.debug(f'cpu stats => {temp_c}, {temp_f}, {usage_percent}')

    def _handle_nics_interface(self, network_id, network_stats):
        ip = network_stats.get(NICSInterfaceDictKeys.IP)
        mac = network_stats.get(NICSInterfaceDictKeys.MAC)
        usage = network_stats.get(NICSInterfaceDictKeys.USAGE)
        max_speed = network_stats.get(NICSInterfaceDictKeys.MAX_SPEED)
        err_packets = network_stats.get(NICSInterfaceDictKeys.ERR_PACKETS)
        rx_packets = network_stats.get(NICSInterfaceDictKeys.RX_PACKETS)
        tx_packets = network_stats.get(NICSInterfaceDictKeys.TX_PACKETS)
        # TODO: add something to check `link_status` and output a 1 or 0
        Metrics.SYSTEM_STATS_NICS_MAX_SPEED.labels(
            network_id=network_id,
            ip=ip,
            mac=mac,
            usage=usage,
        ).set(max_speed)
        Metrics.SYSTEM_STATS_NICS_ERR_PACKETS.labels(
            network_id=network_id,
            ip=ip,
            mac=mac,
            usage=usage,
        ).set(err_packets)
        Metrics.SYSTEM_STATS_NICS_RX_PACKETS.labels(
            network_id=network_id,
            ip=ip,
            mac=mac,
            usage=usage,
        ).set(rx_packets)
        Metrics.SYSTEM_STATS_NICS_TX_PACKETS.labels(
            network_id=network_id,
            ip=ip,
            mac=mac,
            usage=usage,
        ).set(tx_packets)

    def _handle_nics_dict(self, stats):
        nics = stats.get(SystemStatsKeys.NICS)
        if not nics:
            return
        for key, value in nics.items():
            self._handle_nics_interface(key, value)

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
        self._handle_system_dict(stats)

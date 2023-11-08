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


class SystemStatsProcessorException(BaseProcessorException):
    pass


class SystemStatsProcessor(BaseProcessor):
    @classmethod
    def _convert_uptime_dict(cls, uptime_dict):
        log.info(f'starting with uptime_dict: {uptime_dict}')
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
        log.info(f_m)
        return total_seconds

    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_system_stats => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        cpu = stats.get(SystemStatsKeys.CPU)
        if cpu:
            temp_c = cpu.get('temp_c', 0)
            Metrics.SYSTEM_STATS_CPU_TEMP_C_VALUE.set(temp_c)
            temp_f = cpu.get('temp_f', 0)
            Metrics.SYSTEM_STATS_CPU_TEMP_F_VALUE.set(temp_f)
            usage_percent = cpu.get('usage_percent', 0)
            Metrics.SYSTEM_STATS_CPU_USAGE_PERCENT_VALUE.set(usage_percent)
            log.info(f'cpu stats => {temp_c}, {temp_f}, {usage_percent}')
        memory = stats.get(SystemStatsKeys.MEMORY)
        if memory:
            free = memory.get('free', 0)
            Metrics.SYSTEM_STATS_MEMORY_FREE_VALUE.set(free)
            total = memory.get('total', 0)
            Metrics.SYSTEM_STATS_MEMORY_TOTAL_VALUE.set(total)
            log.info(f'memory stats => {free}/{total}')
        uptime = stats.get(SystemStatsKeys.UPTIME)
        log.info(f'uptime: {uptime}')
        uptime_seconds = cls._convert_uptime_dict(uptime)
        Metrics.SYSTEM_STATS_UPTIME_SECONDS.set(uptime_seconds)

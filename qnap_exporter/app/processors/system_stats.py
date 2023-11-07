from flask import current_app as app
from ..metrics import Metrics
from ..common.system_stats_keys import SystemStatsKeys
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SystemStatsProcessorException(BaseProcessorException):
    pass


class SystemStatsProcessor(BaseProcessor):
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

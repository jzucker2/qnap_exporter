from flask import current_app as app
from ..utils import global_get_now
from ..common.domains import Domains
from ..metrics import Metrics


log = app.logger


class DomainStatsException(Exception):
    pass


class InvalidMetricsDomainStatsException(DomainStatsException):
    pass


class SystemStatsKeys(object):
    CPU = 'cpu'
    DNS = 'dns'
    FIRMWARE = 'firmware'
    MEMORY = 'memory'
    NICS = 'nics'
    SYSTEM = 'system'
    UPTIME = 'uptime'


class DomainStats(object):
    @classmethod
    def get_now(cls):
        return global_get_now()

    def __init__(self, domain, domain_func):
        super().__init__()
        self._stats = None
        self._domain = domain
        self._domain_func = domain_func
        self._last_updated = None
        self._created = self.get_now()

    def __repr__(self):
        return (f'DomainStats ==> domain: {self.domain} '
                f'| created: {self.created} | '
                f'last_updated: {self.last_updated} |')

    @property
    def created(self):
        return self._created

    @property
    def last_updated(self):
        return self._last_updated

    def set_last_updated(self, last_updated=None):
        if not last_updated:
            last_updated = self.get_now()
        self._last_updated = last_updated

    @property
    def domain(self):
        return self._domain

    @property
    def domain_name(self):
        return self.domain.value

    @property
    def stats(self):
        return self._stats

    def set_stats(self, stats, last_updated=None):
        self._stats = stats
        self.set_last_updated(last_updated=last_updated)

    @property
    def domain_func(self):
        return self._domain_func

    def update_stats(self, last_updated=None):
        updated_stats = self._domain_func()
        self.set_stats(updated_stats, last_updated=last_updated)

    def update_metrics(self):
        if self.domain == Domains.SYSTEM_STATS:
            self._process_system_stats()
        elif self.domain == Domains.VOLUMES:
            self._process_volumes()
        elif self.domain == Domains.SYSTEM_HEALTH:
            self._process_system_health()
        elif self.domain == Domains.SMART_DISK_HEALTH:
            self._process_smart_disk_health()
        elif self.domain == Domains.BANDWIDTH:
            self._process_bandwidth()
        else:
            e_m = f'update_metrics failed for self.domain: {self.domain}'
            log.error(e_m)
            raise InvalidMetricsDomainStatsException(e_m)

    def _process_system_stats(self):
        stats = self.stats
        m = (f'_process_system_stats => '
             f'stats: {stats} ({self.last_updated})')
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

    def _process_system_health(self):
        stats = self.stats
        m = (f'_process_system_health => '
             f'stats: {stats} ({self.last_updated})')
        log.info(m)

    def _process_volumes(self):
        stats = self.stats
        m = (f'_process_volumes => '
             f'stats: {stats} ({self.last_updated})')
        log.info(m)

    def _process_smart_disk_health(self):
        stats = self.stats
        m = (f'_process_smart_disk_health => '
             f'stats: {stats} ({self.last_updated})')
        log.info(m)

    def _process_bandwidth(self):
        stats = self.stats
        m = (f'_process_bandwidth => '
             f'stats: {stats} ({self.last_updated})')
        log.info(m)

from flask import current_app as app
from ..utils import global_get_now
from ..common.domains import Domains
from ..processors.system_stats import SystemStatsProcessor
from ..processors.system_health import SystemHealthProcessor
from ..processors.smart_disk_health import SmartDiskHealthProcessor
from ..processors.volumes import VolumesProcessor
from ..processors.bandwidth import BandwidthProcessor


log = app.logger


class DomainStatsException(Exception):
    pass


class InvalidMetricsDomainStatsException(DomainStatsException):
    pass


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
        last_updated = self.last_updated
        m = (f'_process_system_stats => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        SystemStatsProcessor.process(stats, last_updated=last_updated)

    def _process_system_health(self):
        stats = self.stats
        last_updated = self.last_updated
        m = (f'_process_system_health => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        SystemHealthProcessor.process(stats, last_updated=last_updated)

    def _process_volumes(self):
        stats = self.stats
        last_updated = self.last_updated
        m = (f'_process_volumes => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        VolumesProcessor.process(stats, last_updated=last_updated)

    def _process_smart_disk_health(self):
        stats = self.stats
        last_updated = self.last_updated
        m = (f'_process_smart_disk_health => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        SmartDiskHealthProcessor.process(stats, last_updated=last_updated)

    def _process_bandwidth(self):
        stats = self.stats
        last_updated = self.last_updated
        m = (f'_process_bandwidth => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        BandwidthProcessor.process(stats, last_updated=last_updated)

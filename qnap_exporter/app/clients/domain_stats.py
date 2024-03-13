from flask import current_app as app
from ..utils import global_get_now
from ..common.domains import Domains
from ..clients.qnap_client import QNAPClientException
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

    def __init__(self, qnap_client, domain):
        super().__init__()
        self._qnap_client = qnap_client
        self._stats = None
        self._domain = domain
        self._last_updated = None
        self._created = self.get_now()

    def __repr__(self):
        return (f'DomainStats ==> domain: {self.domain} '
                f'| created: {self.created} | '
                f'last_updated: {self.last_updated} |')

    @property
    def qnap_client(self):
        return self._qnap_client

    @property
    def nas_name(self):
        return self.qnap_client.nas_name

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
    def _domain_func(self):
        d_m = f'fetching domain func for self.domain: {self.domain}'
        log.debug(d_m)
        if self.domain == Domains.SYSTEM_STATS:
            return self.qnap_client.get_system_stats
        elif self.domain == Domains.VOLUMES:
            return self.qnap_client.get_volumes
        elif self.domain == Domains.SYSTEM_HEALTH:
            return self.qnap_client.get_system_health
        elif self.domain == Domains.SMART_DISK_HEALTH:
            return self.qnap_client.get_smart_disk_health
        elif self.domain == Domains.BANDWIDTH:
            return self.qnap_client.get_bandwidth
        else:
            e_m = f'_domain_func failed for self.domain: {self.domain}'
            log.error(e_m)
            raise InvalidMetricsDomainStatsException(e_m)

    def update_stats(self, last_updated=None):
        # TODO: perfect spot to create empty stats and update,
        #  that way we can 0 out if we can't connect
        try:
            d_m = (f'self.nas_name: {self.nas_name} updating '
                   f'stats for self.domain: {self.domain}')
            log.info(d_m)
            updated_stats = self._domain_func()
            s_m = f'self.domain: {self.domain} updated_stats: {updated_stats}'
            log.debug(s_m)
            self.set_stats(updated_stats, last_updated=last_updated)
        except QNAPClientException as qe:
            q_m = f'update_stats domain: {self.domain_name} => qe: {qe}'
            log.error(q_m)
        except Exception as unexp:
            u_m = f'update_stats domain: {self.domain_name} => unexp: {unexp}'
            log.error(u_m)
        else:
            self.set_stats(updated_stats, last_updated=last_updated)

    def _get_domain_processor(self):
        if self.domain == Domains.SYSTEM_STATS:
            return SystemStatsProcessor.get_processor(self.nas_name)
        elif self.domain == Domains.VOLUMES:
            return VolumesProcessor.get_processor(self.nas_name)
        elif self.domain == Domains.SYSTEM_HEALTH:
            return SystemHealthProcessor.get_processor(self.nas_name)
        elif self.domain == Domains.SMART_DISK_HEALTH:
            return SmartDiskHealthProcessor.get_processor(self.nas_name)
        elif self.domain == Domains.BANDWIDTH:
            return BandwidthProcessor.get_processor(self.nas_name)
        else:
            e_m = f'_domain_processor failed for self.domain: {self.domain}'
            log.error(e_m)
            raise InvalidMetricsDomainStatsException(e_m)

    def update_metrics(self):
        stats = self.stats
        last_updated = self.last_updated
        m = (f'update_metrics => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        processor = self._get_domain_processor()
        processor.process(stats, last_updated=last_updated)

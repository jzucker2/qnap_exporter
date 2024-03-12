from flask import current_app as app
from ..utils import global_get_now
from ..common.domains import Domains
from .domain_stats import DomainStats
from .qnap_client import QNAPClient


log = app.logger


class CollectorException(Exception):
    pass


class Collector(object):
    DEFAULT_SYSTEM_HEALTH_VALUE = 'missing'

    @classmethod
    def get_client(cls, qnap_client=None):
        if not qnap_client:
            qnap_client = QNAPClient.get_client()
        return cls(qnap_client)

    def __init__(self, qnap_client):
        super().__init__()
        self.qnap_client = qnap_client
        self._domains = None
        self._set_up_domains()

    @classmethod
    def get_now(cls):
        return global_get_now()

    def __repr__(self):
        return f'Exporter => domains: {self.domains}'

    def _set_up_domains(self):
        self._domains = {
            Domains.SYSTEM_STATS:
                DomainStats(
                    Domains.SYSTEM_STATS,
                    self.qnap_client.get_system_stats),
            Domains.BANDWIDTH:
                DomainStats(
                    Domains.BANDWIDTH,
                    self.qnap_client.get_bandwidth),
            Domains.VOLUMES:
                DomainStats(
                    Domains.VOLUMES,
                    self.qnap_client.get_volumes),
            Domains.SMART_DISK_HEALTH:
                DomainStats(
                    Domains.SMART_DISK_HEALTH,
                    self.qnap_client.get_smart_disk_health),
            Domains.SYSTEM_HEALTH:
                DomainStats(
                    Domains.SYSTEM_HEALTH,
                    self.qnap_client.get_system_health),
        }

    @property
    def domains(self):
        return self._domains

    def get_domain_stats(self, domain):
        return self.domains[domain]

    def update_domain_stats(self, domain, last_updated=None):
        domain_stats = self.get_domain_stats(domain)
        domain_stats.update_stats(last_updated=last_updated)

    def fetch_all_domains_stats(self, last_updated=None):
        if not last_updated:
            # for a uniform timestamp for all the metrics fetched
            last_updated = self.get_now()
        a_m = f'fetching all domains stats for last_updated: {last_updated}'
        log.info(a_m)
        for domain, domain_stats in self.domains.items():
            d_m = (f'fetching stats for domain: {domain} '
                   f'at last_updated: {last_updated}')
            log.debug(d_m)
            domain_stats.update_stats(last_updated=last_updated)

    def update_all_domains_metrics(self, check_first=True, last_updated=None):
        # FIXME: check for `last_updated` first
        for domain, domain_stats in self.domains.items():
            log.info(f'updating metrics for domain: {domain}')
            domain_stats.update_metrics()

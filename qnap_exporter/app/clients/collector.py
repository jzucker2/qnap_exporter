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
    def get_default_collector(cls, qnap_client=None):
        if not qnap_client:
            qnap_client = QNAPClient.get_default_client()
        return cls(qnap_client)

    @classmethod
    def get_collector(cls, qnap_client):
        return cls(qnap_client)

    def __init__(self, qnap_client):
        super().__init__()
        self._qnap_client = qnap_client
        self._domains = None
        self._set_up_domains()

    @classmethod
    def get_now(cls):
        return global_get_now()

    @property
    def qnap_client(self):
        return self._qnap_client

    @property
    def nas_name(self):
        return self.qnap_client.nas_name

    def __repr__(self):
        m = f'Collector => nas_name: {self.nas_name} domains: {self.domains}'
        return m

    def _set_up_domains(self):
        # FIXME: this is repetitive
        self._domains = {
            Domains.SYSTEM_STATS:
                DomainStats(
                    self.qnap_client,
                    Domains.SYSTEM_STATS),
            Domains.BANDWIDTH:
                DomainStats(
                    self.qnap_client,
                    Domains.BANDWIDTH),
            Domains.VOLUMES:
                DomainStats(
                    self.qnap_client,
                    Domains.VOLUMES),
            Domains.SMART_DISK_HEALTH:
                DomainStats(
                    self.qnap_client,
                    Domains.SMART_DISK_HEALTH),
            Domains.SYSTEM_HEALTH:
                DomainStats(
                    self.qnap_client,
                    Domains.SYSTEM_HEALTH),
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
            log.info(d_m)
            domain_stats.update_stats(last_updated=last_updated)

    def update_all_domains_metrics(self, check_first=True, last_updated=None):
        # FIXME: check for `last_updated` first
        for domain, domain_stats in self.domains.items():
            log.debug(f'updating metrics for domain: {domain}')
            domain_stats.update_metrics()

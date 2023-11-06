from datetime import datetime
from flask import current_app as app
from ..common.domains import Domains
from .qnap_client import QNAPClient


log = app.logger


class DomainStats(object):
    @classmethod
    def get_now(cls):
        return datetime.utcnow()

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

    @property
    def domain(self):
        return self._domain

    @property
    def domain_name(self):
        return self.domain.value

    @property
    def stats(self):
        return self._stats

    def set_stats(self, stats):
        self._stats = stats
        self._last_updated = self.get_now()

    @property
    def domain_func(self):
        return self._domain_func

    def update_stats(self):
        updated_stats = self._domain_func()
        self.set_stats(updated_stats)


class ExporterException(Exception):
    pass


class Exporter(object):
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

    def update_domain_stats(self, domain):
        domain_stats = self.get_domain_stats(domain)
        domain_stats.update_stats()

    def update_all_domains(self):
        for domain, domain_stats in self.domains.items():
            log.info(f'updating stats for domain: {domain}')
            domain_stats.update_stats()

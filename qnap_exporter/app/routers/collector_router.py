from flask import current_app as app
from ..common.config_keys import ConfigKeys
from ..clients.qnap_client import QNAPClient
from ..clients.env_vars import EnvVars
from ..clients.config_parser import ConfigParser
from ..clients.collector import Collector
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class CollectorRouterException(RouterException):
    pass


class CollectorRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = ConfigParser.import_config()
        log.debug(f'config: {config}')
        self.collector = self._create_env_var_collector()
        self.config = config
        self._collectors = None

    @property
    def service(self):
        return 'collector'

    @property
    def collectors(self):
        if not self._collectors:
            collectors = self.create_collectors(self.config)
            self._collectors = list(collectors)
        return self._collectors

    @classmethod
    def _has_qnap_config_env_vars(cls):
        return EnvVars.has_qnap_nas_config_env_vars()

    @classmethod
    def should_use_config_file(cls):
        if cls._has_qnap_config_env_vars():
            return False
        return True

    @classmethod
    def _create_env_var_collector(cls):
        return Collector.get_default_collector()

    @classmethod
    def _create_collector_from_config(cls, nas_config):
        nas_name = nas_config[ConfigKeys.NAS_NAME.key_name]
        nas_ip = nas_config[ConfigKeys.NAS_IP.key_name]
        nas_port = nas_config[ConfigKeys.NAS_PORT]
        nas_username = nas_config[ConfigKeys.NAS_USERNAME]
        nas_password = nas_config[ConfigKeys.NAS_PASSWORD.key_name]
        qnap_client = QNAPClient.get_collecting_client(
            nas_name,
            nas_ip,
            nas_port,
            nas_username,
            nas_password)
        collector = Collector.get_collector(qnap_client)
        return collector

    @classmethod
    def create_collectors(cls, config):
        collectors = []
        if cls.should_use_config_file():
            log.debug('Using yml config file for router configs')
            nas_instances = ConfigParser.get_all_nas_instances(config)
            for nas_config in nas_instances:
                collector = cls._create_collector_from_config(nas_config)
                collectors.append(collector)
            return list(collectors)
        else:
            log.debug('Using env vars for router configs')
            collector = cls._create_env_var_collector()
            collectors.append(collector)
        return list(collectors)

    @property
    def nas_name(self):
        return self.collector.nas_name

    def handle_simple_collector_route_response(self):
        with Metrics.SIMPLE_COLLECTOR_ROUTE_TIME.labels(
            nas_name=self.nas_name,
        ).time():
            with Metrics.SIMPLE_COLLECTOR_ROUTE_EXCEPTIONS.labels(
                nas_name=self.nas_name,
            ).count_exceptions():
                p_m = 'handle simple collector route'
                log.debug(p_m)
                final_response = self.base_response('simple')
                self.collector.fetch_all_domains_stats()
                log.debug(f'self.collector: {self.collector}')
                return final_response

    def handle_collector_metrics_update_route_response(self):
        with Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_TIME.labels(
            nas_name=self.nas_name,
        ).time():
            with Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_EXCEPTIONS.labels(
                nas_name=self.nas_name,
            ).count_exceptions():
                p_m = 'handle collector metrics update route'
                log.debug(p_m)
                final_response = self.base_response('metrics_update')
                for collector in self.collectors:
                    c_f = (f'collector: {collector} first '
                           f'fetch the domains stats')
                    log.debug(c_f)
                    collector.fetch_all_domains_stats()
                    u_m = (f'collector: {collector} now that we '
                           f'fetched the latest stats, update metrics')
                    log.debug(u_m)
                    collector.update_all_domains_metrics()
                    d_m = (f'collector: {collector} now done '
                           f'with both stats and metrics')
                    log.debug(d_m)
                    return final_response

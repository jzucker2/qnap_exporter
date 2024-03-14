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
        self.collector = self._create_env_var_collector()
        self._collectors = None
        self._config = None

    @property
    def config(self):
        if not self._config:
            self._config = ConfigParser.import_config()
        return self._config

    @property
    def service(self):
        return 'collector'

    @property
    def collectors(self):
        if not self._collectors:
            collectors = self._create_collectors()
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
        log.debug(f'nas_config: {nas_config}')
        nas_name = nas_config[ConfigKeys.NAS_NAME.key_name]
        nas_host = nas_config[ConfigKeys.NAS_HOST.key_name]
        nas_port = nas_config[ConfigKeys.NAS_PORT.key_name]
        nas_username = nas_config[ConfigKeys.NAS_USERNAME.key_name]
        nas_password = nas_config[ConfigKeys.NAS_PASSWORD.key_name]
        qnap_client = QNAPClient.get_collecting_client(
            nas_name,
            nas_host,
            nas_port,
            nas_username,
            nas_password)
        collector = Collector.get_collector(qnap_client)
        return collector

    def _get_all_nas_instances_from_config(self):
        config = self.config
        return ConfigParser.get_all_nas_instances(config)

    def _create_collectors(self):
        collectors = []
        if self.should_use_config_file():
            log.debug('Using yml config file for router configs')
            nas_instances = self._get_all_nas_instances_from_config()
            log.debug(f'nas_instances: {nas_instances}')
            for nas_config in nas_instances:
                collector = self._create_collector_from_config(nas_config)
                collectors.append(collector)
        else:
            log.debug('Using env vars for router configs')
            collector = self._create_env_var_collector()
            collectors.append(collector)
        log.debug(f'collectors: {collectors}')
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

    def _handle_collector_metrics_update(self, collector):
        nas_name = collector.nas_name
        log.debug(f'collector: {collector} nas_name: {nas_name}')
        with Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_TIME.labels(
            nas_name=nas_name,
        ).time():
            with Metrics.COLLECTOR_METRICS_UPDATE_ROUTE_EXCEPTIONS.labels(
                nas_name=nas_name,
            ).count_exceptions():
                p_m = 'handle collector metrics update route'
                log.debug(p_m)
                collector_response = self.base_response('metrics_update')
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
                return collector_response

    def handle_all_collectors_metrics_update_route_response(self):
        p_m = 'handle collector metrics update route'
        log.debug(p_m)
        final_response = self.base_response('metrics_update')
        for collector in self.collectors:
            response = self._handle_collector_metrics_update(collector)
            cr_m = f'collector: {collector} had response: {response}'
            log.debug(cr_m)
        return final_response

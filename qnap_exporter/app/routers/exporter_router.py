from flask import current_app as app
from ..clients.exporter import Exporter
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class ExporterRouterException(RouterException):
    pass


class ExporterRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exporter = Exporter.get_client()

    @property
    def service(self):
        return 'exporter'

    @Metrics.SIMPLE_EXPORTER_ROUTE_TIME.time()
    def handle_simple_exporter_route_response(self):
        with Metrics.SIMPLE_EXPORTER_ROUTE_EXCEPTIONS.count_exceptions():
            p_m = 'handle simple exporter route'
            log.debug(p_m)
            final_response = self.base_response('simple')
            self.exporter.fetch_all_domains_stats()
            log.debug(f'self.exporter: {self.exporter}')
            return final_response

    @Metrics.EXPORTER_METRICS_UPDATE_ROUTE_TIME.time()
    def handle_exporter_metrics_update_route_response(self):
        with Metrics.EXPORTER_METRICS_UPDATE_ROUTE_EXCEPTIONS.count_exceptions():  # noqa: E501
            p_m = 'handle exporter metrics update route'
            log.debug(p_m)
            final_response = self.base_response('metrics_update')
            log.debug('first fetch the domains stats')
            self.exporter.fetch_all_domains_stats()
            log.debug('now that we fetched the latest stats, update metrics')
            self.exporter.update_all_domains_metrics()
            log.debug('done with both stats and metrics')
            log.debug(f'self.exporter: {self.exporter}')
            return final_response

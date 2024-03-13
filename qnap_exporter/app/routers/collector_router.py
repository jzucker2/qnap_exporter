from flask import current_app as app
from ..clients.collector import Collector
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class CollectorRouterException(RouterException):
    pass


class CollectorRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collector = Collector.get_default_client()

    @property
    def service(self):
        return 'collector'

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
                log.debug('first fetch the domains stats')
                self.collector.fetch_all_domains_stats()
                u_m = 'now that we fetched the latest stats, update metrics'
                log.debug(u_m)
                self.collector.update_all_domains_metrics()
                log.debug('done with both stats and metrics')
                log.debug(f'self.collector: {self.collector}')
                return final_response

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
            log.info(p_m)
            final_response = self.base_response('simple_exporter')
            self.exporter.update_all_domains()
            log.info(f'self.exporter: {self.exporter}')
            return final_response

from flask import current_app as app
from ..clients.qnap_client import QNAPClient
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class DebugRouterException(RouterException):
    pass


class DebugRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.qnap_client = QNAPClient.get_client()

    @property
    def service(self):
        return 'debug'

    @Metrics.DEBUG_ROUTE_TIME.time()
    def handle_debug_route_response(self):
        with Metrics.DEBUG_ROUTE_EXCEPTIONS.count_exceptions():
            p_m = 'handle debug route'
            log.info(p_m)
            final_response = self.base_response('debug_route')
            stats = self.qnap_client.get_system_stats()
            log.info(f'stats: {stats}')
            return final_response

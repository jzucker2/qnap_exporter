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
            system_stats = self.qnap_client.get_system_stats()
            log.info(f'system_stats: {system_stats}')
            if system_stats:
                final_response['system_stats'] = system_stats
            system_health = self.qnap_client.get_system_health()
            log.info(f'system_health: {system_health}')
            if system_health:
                final_response['system_health'] = system_health
            bandwidth = self.qnap_client.get_bandwidth()
            log.info(f'bandwidth: {bandwidth}')
            if bandwidth:
                final_response['bandwidth'] = bandwidth
            volumes = self.qnap_client.get_volumes()
            log.info(f'volumes: {volumes}')
            if volumes:
                final_response['volumes'] = volumes
            # firmware_update = self.qnap_client.get_firmware_update()
            # log.info(f'firmware_update: {firmware_update}')
            # if firmware_update:
            #     final_response['firmware_update'] = firmware_update
            smart_disk_health = self.qnap_client.get_smart_disk_health()
            log.info(f'smart_disk_health: {smart_disk_health}')
            if smart_disk_health:
                final_response['smart_disk_health'] = smart_disk_health
            return final_response

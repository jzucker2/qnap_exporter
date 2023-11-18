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
            log.debug(p_m)
            final_response = self.base_response('debug')
            system_stats = self.qnap_client.get_system_stats()
            log.debug(f'system_stats: {system_stats}')
            if system_stats:
                final_response['system_stats'] = system_stats
            system_health = self.qnap_client.get_system_health()
            log.debug(f'system_health: {system_health}')
            if system_health:
                final_response['system_health'] = system_health
            bandwidth = self.qnap_client.get_bandwidth()
            log.debug(f'bandwidth: {bandwidth}')
            if bandwidth:
                final_response['bandwidth'] = bandwidth
            volumes = self.qnap_client.get_volumes()
            log.debug(f'volumes: {volumes}')
            if volumes:
                final_response['volumes'] = volumes
            firmware_update = self.qnap_client.get_firmware_update()
            log.debug(f'firmware_update: {firmware_update}')
            if firmware_update:
                final_response['firmware_update'] = firmware_update
            smart_disk_health = self.qnap_client.get_smart_disk_health()
            log.debug(f'smart_disk_health: {smart_disk_health}')
            if smart_disk_health:
                final_response['smart_disk_health'] = smart_disk_health
            return final_response

    @Metrics.DEBUG_ROUTE_TIME.time()
    def handle_debug_pprint_route_response(self):
        with Metrics.DEBUG_ROUTE_EXCEPTIONS.count_exceptions():
            import pprint
            p_m = 'handle debug print route'
            log.debug(p_m)
            final_response = self.base_response('debug_pprint')
            system_stats = self.qnap_client.get_system_stats()
            log.debug(f'system_stats: {system_stats}')
            pprint.pprint(system_stats)
            if system_stats:
                final_response['system_stats'] = system_stats
            system_health = self.qnap_client.get_system_health()
            log.debug(f'system_health: {system_health}')
            pprint.pprint(system_health)
            if system_health:
                final_response['system_health'] = system_health
            bandwidth = self.qnap_client.get_bandwidth()
            log.debug(f'bandwidth: {bandwidth}')
            pprint.pprint(bandwidth)
            if bandwidth:
                final_response['bandwidth'] = bandwidth
            volumes = self.qnap_client.get_volumes()
            log.debug(f'volumes: {volumes}')
            pprint.pprint(volumes)
            if volumes:
                final_response['volumes'] = volumes
            # firmware_update = self.qnap_client.get_firmware_update()
            # log.debug(f'firmware_update: {firmware_update}')
            # pprint.pprint(firmware_update)
            # if firmware_update:
            #     final_response['firmware_update'] = firmware_update
            smart_disk_health = self.qnap_client.get_smart_disk_health()
            log.debug(f'smart_disk_health: {smart_disk_health}')
            pprint.pprint(smart_disk_health)
            if smart_disk_health:
                final_response['smart_disk_health'] = smart_disk_health
            return final_response

    @Metrics.DEBUG_ROUTE_TIME.time()
    def handle_debug_firmware_update_route_response(self):
        with Metrics.DEBUG_ROUTE_EXCEPTIONS.count_exceptions():
            import pprint
            p_m = 'handle debug firmware update route'
            log.info(p_m)
            final_response = self.base_response('debug_firmware_update')
            firmware_update = self.qnap_client.safe_get_debug_firmware_update()
            log.debug(f'firmware_update: {firmware_update}')
            pprint.pprint(firmware_update)
            if firmware_update:
                final_response['firmware_update'] = firmware_update
            return final_response

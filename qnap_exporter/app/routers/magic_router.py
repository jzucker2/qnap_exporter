from flask import current_app as app
from ..clients.wake_on_lan import (WakeOnLan, WakeOnLanException)
from ..metrics import Metrics
from .router import Router, RouterException


log = app.logger


class MagicRouterException(RouterException):
    pass


class MagicRouter(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wake_on_lan_client = WakeOnLan.get_client()

    @property
    def service(self):
        return 'magic'

    async def _wake_on_lan(self, mac_address, ip_address, delay_after_wake=0):
        wol_m = f'try sending magic packet to ' \
                f'mac_address: {mac_address} and ' \
                f'ip_address: {ip_address}'
        log.info(wol_m)
        try:
            await self.wake_on_lan_client.wake_up(
                mac_address,
                ip_address,
                delay_after_wake=delay_after_wake)
        except WakeOnLanException as oe:
            raise MagicRouterException(f'Wake on lan issue => {oe}') from oe
        except Exception as e:
            raise MagicRouterException(f'Got other exception: {e}') from e
        log.info('sent magic packet')

    @Metrics.SEND_MAGIC_PACKET_TIME.time()
    async def send_magic_packet_response(self):
        with Metrics.SEND_MAGIC_PACKET_EXCEPTIONS.count_exceptions():
            request_body = self.get_request_json()
            mac_address = request_body['mac_address']
            ip_address = request_body['ip_address']
            p_m = f'send magic packet for request_body: {request_body}'
            log.info(p_m)
            final_response = self.base_response('wal_send_magic_packet')
            await self._wake_on_lan(mac_address, ip_address)
            return final_response

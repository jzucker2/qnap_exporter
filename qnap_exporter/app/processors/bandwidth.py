from flask import current_app as app
from ..metrics import Metrics
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class NetworkInterfaceDictKeys(object):
    NAME = 'name'
    RX = 'rx'
    TX = 'tx'
    IS_DEFAULT = 'is_default'


class BandwidthProcessorException(BaseProcessorException):
    pass


class BandwidthProcessor(BaseProcessor):
    @classmethod
    def _handle_network_interface(cls, network_id, network_stats):
        h_m = (f'_handle_network interface for '
               f'network_id: {network_id} with '
               f'network_stats: {network_stats}')
        log.debug(h_m)
        name = network_stats.get(NetworkInterfaceDictKeys.NAME)
        rx = network_stats.get(NetworkInterfaceDictKeys.RX, 0)
        tx = network_stats.get(NetworkInterfaceDictKeys.TX, 0)
        is_default = network_stats.get(NetworkInterfaceDictKeys.IS_DEFAULT)
        Metrics.BANDWIDTH_INTERFACE_RX.labels(
            network_id=network_id,
            network_name=name,
            is_default=is_default,
        ).set(rx)
        Metrics.BANDWIDTH_INTERFACE_TX.labels(
            network_id=network_id,
            network_name=name,
            is_default=is_default,
        ).set(tx)

    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_bandwidth => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return
        for key, value in stats.items():
            cls._handle_network_interface(key, value)

from flask import current_app as app
from ..common.bandwidth_transfer_types import BandwidthTransferTypes
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


class InvalidTransferTypeProcessorException(BandwidthProcessorException):
    pass


class BandwidthProcessor(BaseProcessor):
    def _get_rate(self, transfer_type, network_stats):
        rate_key = None
        if transfer_type == BandwidthTransferTypes.TX:
            rate_key = NetworkInterfaceDictKeys.TX
        elif transfer_type == BandwidthTransferTypes.RX:
            rate_key = NetworkInterfaceDictKeys.RX
        else:
            e_m = f'Invalid transfer_type: {transfer_type}'
            log.error(e_m)
            raise InvalidTransferTypeProcessorException(e_m)
        final_rate = network_stats.get(rate_key, 0)
        t_m = f'transfer_type: {transfer_type} got final_rate: {final_rate}'
        log.debug(t_m)
        return final_rate

    def _handle_network_interface(self, network_id, network_stats):
        h_m = (f'_handle_network interface for '
               f'network_id: {network_id} with '
               f'network_stats: {network_stats}')
        log.debug(h_m)
        name = network_stats.get(NetworkInterfaceDictKeys.NAME)
        is_default = network_stats.get(NetworkInterfaceDictKeys.IS_DEFAULT)
        for transfer_type in BandwidthTransferTypes.bandwidth_metrics_list():
            rate = self._get_rate(transfer_type, network_stats)
            Metrics.BANDWIDTH_INTERFACE_TRANSFER_RATE.labels(
                nas_name=self.nas_name,
                network_id=network_id,
                network_name=name,
                is_default=is_default,
                transfer_type=transfer_type.label_string,
            ).set(rate)

    def process(self, stats, last_updated=None):
        m = (f'_process_bandwidth => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return
        for key, value in stats.items():
            self._handle_network_interface(key, value)

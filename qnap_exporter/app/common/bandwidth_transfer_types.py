from enum import Enum


class BandwidthTransferTypes(Enum):
    TX = 'tx'
    RX = 'rx'
    ERR = 'err'

    @property
    def label_string(self):
        return self.value

    @classmethod
    def bandwidth_metrics_list(cls):
        return list([
            cls.TX,
            cls.RX,
            cls.ERR,
        ])

    @classmethod
    def nics_packet_metrics_list(cls):
        return list([
            cls.TX,
            cls.RX,
            cls.ERR,
        ])

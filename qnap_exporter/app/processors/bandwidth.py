from flask import current_app as app
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class BandwidthProcessorException(BaseProcessorException):
    pass


class BandwidthProcessor(BaseProcessor):
    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_bandwidth => '
             f'stats: {stats} ({last_updated})')
        log.info(m)

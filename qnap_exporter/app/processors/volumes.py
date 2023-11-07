from flask import current_app as app
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class VolumesProcessorException(BaseProcessorException):
    pass


class VolumesProcessor(BaseProcessor):
    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_volumes => '
             f'stats: {stats} ({last_updated})')
        log.info(m)

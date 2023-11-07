from flask import current_app as app
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SmartDiskHealthProcessorException(BaseProcessorException):
    pass


class SmartDiskHealthProcessor(BaseProcessor):
    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_smart_disk_health => '
             f'stats: {stats} ({last_updated})')
        log.info(m)

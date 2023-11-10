from flask import current_app as app
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SystemHealthProcessorException(BaseProcessorException):
    pass


class SystemHealthProcessor(BaseProcessor):
    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_system_health => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)

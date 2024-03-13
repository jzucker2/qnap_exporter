from flask import current_app as app
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SystemHealthProcessorException(BaseProcessorException):
    pass


class SystemHealthProcessor(BaseProcessor):
    def process(self, stats, last_updated=None):
        m = (f'_process_system_health => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return

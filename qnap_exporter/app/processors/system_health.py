from flask import current_app as app
from ..metrics import Metrics
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SystemHealthProcessorException(BaseProcessorException):
    pass


class SystemHealthProcessor(BaseProcessor):
    def process(self, stats, last_updated=None):
        m = (f'_process_system_health => '
             f'stats: {stats} ({last_updated}) of '
             f'type(stats): {type(stats)}')
        log.debug(m)
        if not stats:
            return
        final_status = str(stats)
        Metrics.SYSTEM_HEALTH_STATUS.labels(
            nas_name=self.nas_name,
            system_health_status=final_status
        ).set(1)

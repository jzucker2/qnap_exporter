from flask import current_app as app
from ..metrics import Metrics
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class VolumeDictKeys(object):
    FOLDERS = 'folders'
    FREE_SIZE = 'free_size'
    ID_NUMBER = 'id'
    LABEL = 'label'
    TOTAL_SIZE = 'total_size'


class VolumesProcessorException(BaseProcessorException):
    pass


class VolumesProcessor(BaseProcessor):
    @classmethod
    def _handle_volume(cls, volume_id, volume_stats):
        if not volume_stats:
            return
        id_number = volume_stats.get(VolumeDictKeys.ID_NUMBER)
        label = volume_stats.get(VolumeDictKeys.LABEL)
        free_size = volume_stats.get(VolumeDictKeys.FREE_SIZE)
        total_size = volume_stats.get(VolumeDictKeys.TOTAL_SIZE)
        Metrics.VOLUME_FREE_SIZE.labels(
            volume_id=volume_id,
            volume_id_number=id_number,
            volume_label=label,
        ).set(free_size)
        Metrics.VOLUME_TOTAL_SIZE.labels(
            volume_id=volume_id,
            volume_id_number=id_number,
            volume_label=label,
        ).set(total_size)

    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_volumes => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        for key, value in stats.items():
            cls._handle_volume(key, value)

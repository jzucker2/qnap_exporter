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


class FolderDictKeys(object):
    SHARENAME = 'sharename'
    USED_SIZE = 'used_size'


class VolumesProcessorException(BaseProcessorException):
    pass


class VolumesProcessor(BaseProcessor):
    @classmethod
    def _handle_folder(cls, id, id_number, label, folder_stats):
        if not folder_stats:
            return
        sharename = folder_stats.get(FolderDictKeys.SHARENAME)
        used_size = folder_stats.get(FolderDictKeys.USED_SIZE)
        Metrics.VOLUME_FOLDER_USED_SIZE.labels(
            volume_id=id,
            volume_id_number=id_number,
            volume_label=label,
            sharename=sharename,
        ).set(used_size)

    @classmethod
    def _iterate_volume_folders(cls, id, id_number, label, volume_stats):
        folders = volume_stats.get(VolumeDictKeys.FOLDERS)
        if not folders:
            return
        for folder_stats in folders:
            cls._handle_folder(id, id_number, label, folder_stats)

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
        cls._iterate_volume_folders(volume_id, id_number, label, volume_stats)

    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_volumes => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        for key, value in stats.items():
            cls._handle_volume(key, value)

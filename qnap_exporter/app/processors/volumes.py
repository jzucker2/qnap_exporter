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
    # @classmethod
    def _handle_folder(self, id, id_number, label, folder_stats):
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

    # @classmethod
    def _iterate_volume_folders(self, id, id_number, label, volume_stats):
        folders = volume_stats.get(VolumeDictKeys.FOLDERS)
        if not folders:
            return
        for folder_stats in folders:
            self._handle_folder(id, id_number, label, folder_stats)

    # @classmethod
    def _handle_volume(self, volume_id, volume_stats):
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
        used_size = total_size - free_size
        Metrics.VOLUME_USED_SIZE.labels(
            volume_id=volume_id,
            volume_id_number=id_number,
            volume_label=label,
        ).set(used_size)
        usage = (used_size / total_size) * 100
        u_m = (f'_handle_volume ({volume_id}) got '
               f'usage: {usage} from ({used_size}/{total_size})')
        log.debug(u_m)
        Metrics.VOLUME_USAGE_PERCENT.labels(
            volume_id=volume_id,
            volume_id_number=id_number,
            volume_label=label,
        ).set(usage)
        # TODO: pass in size values so we can calculate the folder percentages
        self._iterate_volume_folders(volume_id, id_number, label, volume_stats)

    # @classmethod
    def process(self, stats, last_updated=None):
        m = (f'_process_volumes => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return
        for key, value in stats.items():
            self._handle_volume(key, value)

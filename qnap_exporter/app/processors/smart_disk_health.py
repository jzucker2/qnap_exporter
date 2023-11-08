from flask import current_app as app
from ..metrics import Metrics
from .base_processor import BaseProcessorException, BaseProcessor


log = app.logger


class SmartDiskDictKeys(object):
    CAPACITY = 'capacity'
    DRIVE_NUMBER = 'drive_number'
    HEALTH = 'health'
    MODEL = 'model'
    SERIAL = 'serial'
    TEMP_C = 'temp_c'
    TEMP_F = 'temp_f'
    TYPE = 'type'


class SmartDiskHealthProcessorException(BaseProcessorException):
    pass


class SmartDiskHealthProcessor(BaseProcessor):
    @classmethod
    def _handle_smart_disk(cls, smart_disk_id, smart_disk_stats):
        if not smart_disk_stats:
            return
        # TODO: add capacity (probably need to convert something)
        # capacity = smart_disk_stats.get(SmartDiskDictKeys.CAPACITY)
        drive_number = smart_disk_stats.get(SmartDiskDictKeys.DRIVE_NUMBER)
        model = smart_disk_stats.get(SmartDiskDictKeys.MODEL)
        temp_c = smart_disk_stats.get(SmartDiskDictKeys.TEMP_C)
        temp_f = smart_disk_stats.get(SmartDiskDictKeys.TEMP_F)
        disk_type = smart_disk_stats.get(SmartDiskDictKeys.TYPE)
        Metrics.SMART_DISK_HEALTH_TEMP_C_VALUE.labels(
            disk_id=smart_disk_id,
            drive_number=drive_number,
            model=model,
            disk_type=disk_type,
        ).set(temp_c)
        Metrics.SMART_DISK_HEALTH_TEMP_F_VALUE.labels(
            disk_id=smart_disk_id,
            drive_number=drive_number,
            model=model,
            disk_type=disk_type,
        ).set(temp_f)

    @classmethod
    def process(cls, stats, last_updated=None):
        m = (f'_process_smart_disk_health => '
             f'stats: {stats} ({last_updated})')
        log.info(m)
        for key, value in stats.items():
            cls._handle_smart_disk(key, value)

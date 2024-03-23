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
    def _process_capacity(self, disk_id, disk_stats):
        capacity = disk_stats.get(SmartDiskDictKeys.CAPACITY)
        capacity_pieces = capacity.split(' ')
        size = capacity_pieces[0]
        units = capacity_pieces[1]
        c_m = (f'for disk_id: {disk_id} got '
               f'size: {size} for units: {units}')
        log.debug(c_m)
        return size, units

    def _handle_smart_disk(self, smart_disk_id, smart_disk_stats):
        if not smart_disk_stats:
            return
        drive_number = smart_disk_stats.get(SmartDiskDictKeys.DRIVE_NUMBER)
        model = smart_disk_stats.get(SmartDiskDictKeys.MODEL)
        serial = smart_disk_stats.get(SmartDiskDictKeys.SERIAL)
        temp_c = smart_disk_stats.get(SmartDiskDictKeys.TEMP_C)
        temp_f = smart_disk_stats.get(SmartDiskDictKeys.TEMP_F)
        disk_type = smart_disk_stats.get(SmartDiskDictKeys.TYPE)
        health = smart_disk_stats.get(SmartDiskDictKeys.HEALTH)
        log.debug(f'drive_number: {drive_number} got health: {health}')
        Metrics.SMART_DISK_HEALTH_TEMP_C_VALUE.labels(
            nas_name=self.nas_name,
            disk_id=smart_disk_id,
            drive_number=drive_number,
            model=model,
            serial=serial,
            disk_type=disk_type,
            disk_health=health,
        ).set(temp_c)
        Metrics.SMART_DISK_HEALTH_TEMP_F_VALUE.labels(
            nas_name=self.nas_name,
            disk_id=smart_disk_id,
            drive_number=drive_number,
            model=model,
            serial=serial,
            disk_type=disk_type,
            disk_health=health,
        ).set(temp_f)
        capacity, units = self._process_capacity(
            smart_disk_id,
            smart_disk_stats)
        Metrics.SMART_DISK_HEALTH_CAPACITY_VALUE.labels(
            nas_name=self.nas_name,
            disk_id=smart_disk_id,
            drive_number=drive_number,
            model=model,
            serial=serial,
            disk_type=disk_type,
            units=units,
            disk_health=health,
        ).set(capacity)

    def process(self, stats, last_updated=None):
        m = (f'_process_smart_disk_health => '
             f'stats: {stats} ({last_updated})')
        log.debug(m)
        if not stats:
            return
        for key, value in stats.items():
            self._handle_smart_disk(key, value)

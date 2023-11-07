from enum import Enum


class Domains(Enum):
    SYSTEM_HEALTH = 'system_health'
    VOLUMES = 'volumes'
    BANDWIDTH = 'bandwidth'
    SYSTEM_STATS = 'system_stats'
    SMART_DISK_HEALTH = 'smart_disk_health'
    FIRMWARE_UPDATE = 'firmware_update'

    @classmethod
    def all_domains(cls):
        return list([d for d in cls])

    @classmethod
    def all_domains_names(cls):
        return list([d.value for d in cls])

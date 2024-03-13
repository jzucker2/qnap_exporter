from enum import Enum


class ConfigKeys(Enum):
    NAS_INSTANCES = 'nas_instances'
    NAS_NAME = 'nas_name'
    NAS_IP = 'nas_ip'
    NAS_USERNAME = 'nas_username'
    NAS_PASSWORD = 'nas_password'

    @property
    def key_name(self):
        return self.value

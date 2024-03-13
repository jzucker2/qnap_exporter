import os
import yaml
from flask import current_app as app
from ..common.config_keys import ConfigKeys


log = app.logger


class ConfigParserException(Exception):
    pass


class ConfigParser(object):
    DEFAULT_CONFIG_FILE_NAME = 'exporter_config.yaml'
    DEFAULT_CONFIG_FILE_PATH = '/etc/qnap_exporter'

    @classmethod
    def get_config_file_path(cls):
        return os.path.join(
            cls.DEFAULT_CONFIG_FILE_PATH,
            cls.DEFAULT_CONFIG_FILE_NAME)

    @classmethod
    def get_config_file(cls, config_file_path=None):
        if not config_file_path:
            config_file_path = cls.get_config_file_path()
        with open(config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            return config

    @classmethod
    def import_config(cls, config_file_path=None):
        config = cls.get_config_file(config_file_path=config_file_path)
        return config

    @classmethod
    def get_all_nas_instances(cls, config):
        return config[ConfigKeys.NAS_INSTANCES.key_name]

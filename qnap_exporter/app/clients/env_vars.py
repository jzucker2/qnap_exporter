import os


QNAP_NAS_IP = os.environ.get('QNAP_NAS_IP')
QNAP_NAS_NAME = os.environ.get('QNAP_NAS_NAME', 'default')
QNAP_NAS_USERNAME = os.environ.get('QNAP_NAS_USERNAME')
QNAP_NAS_PASSWORD = os.environ.get('QNAP_NAS_PASSWORD')


class EnvVars(object):
    @classmethod
    def get_default_qnap_nas_ip(cls):
        return QNAP_NAS_IP

    @classmethod
    def get_default_qnap_nas_name(cls):
        return QNAP_NAS_NAME

    @classmethod
    def get_default_qnap_nas_username(cls):
        return QNAP_NAS_USERNAME

    @classmethod
    def get_default_qnap_nas_password(cls):
        return QNAP_NAS_PASSWORD

    @classmethod
    def has_qnap_nas_config_env_vars(cls):
        qnap_nas_ip = cls.get_default_qnap_nas_ip()
        if not qnap_nas_ip:
            return False
        qnap_nas_password = cls.get_default_qnap_nas_password()
        if not qnap_nas_password:
            return False
        return True

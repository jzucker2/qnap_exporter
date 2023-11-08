from flask import current_app as app


log = app.logger


class BaseProcessorException(Exception):
    pass


class BaseProcessNotImplementedException(BaseProcessorException):
    pass


class BaseProcessor(object):
    @classmethod
    def get_client(cls):
        return cls()

    @classmethod
    def process(cls, stats, last_updated=None):
        e_m = f'{cls} no process implemented!'
        log.error(e_m)
        raise BaseProcessNotImplementedException(e_m)

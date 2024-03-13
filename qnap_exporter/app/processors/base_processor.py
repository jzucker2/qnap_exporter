from flask import current_app as app


log = app.logger


class BaseProcessorException(Exception):
    pass


class BaseProcessNotImplementedException(BaseProcessorException):
    pass


class BaseProcessor(object):
    @classmethod
    def get_processor(cls, nas_name):
        return cls(nas_name)

    def __init__(self, nas_name):
        super().__init__()
        self._nas_name = nas_name

    @property
    def nas_name(self):
        return self._nas_name

    # @classmethod
    def process(self, stats, last_updated=None):
        e_m = f'{self} no process implemented!'
        log.error(e_m)
        raise BaseProcessNotImplementedException(e_m)

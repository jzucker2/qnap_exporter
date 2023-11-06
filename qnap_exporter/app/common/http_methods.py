from enum import Enum


class HTTPMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'

    DEFAULT = GET

from enum import Enum
from uuid import uuid4
from datetime import datetime
from asgiref.sync import sync_to_async
import logging
from .version import version


class NormalizeIntegerException(Exception):
    pass


convert_to_async = sync_to_async


def set_up_logging(level=logging.DEBUG):
    format = "[%(levelname)s] %(asctime)s %(message)s"
    logging.basicConfig(format=format, level=level)


# pass in __name__
def get_logger(name):
    try:
        from flask import current_app as app
    except ImportError:
        print('import error, using a system logger')
        return logging.getLogger(name)
    return app.logger


ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
SIMPLE_UPLOAD_FORMAT = "%Y-%m-%d %H:%M:%S"
UPLOAD_FORMAT = "%Y-%m-%d %H:%M:%S%z"


# FIXME: https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat  # noqa: E501
def get_iso_datetime_string(dt, format=ISO_FORMAT):
    if not dt:
        return None
    if isinstance(dt, str):
        return dt
    return dt.strftime(format)


def get_iso_datetime(input,
                     format=UPLOAD_FORMAT,
                     backup_format=SIMPLE_UPLOAD_FORMAT):
    if not input:
        return None
    if isinstance(input, datetime):
        return input
    dt = None
    try:
        dt = datetime.strptime(input, format)
    except ValueError:
        dt = datetime.strptime(input, backup_format)
    finally:
        return dt


def global_get_now():
    return datetime.utcnow()


def memory_address(a_obj):
    return id(a_obj)


def hex_address(a_obj):
    return str(hex(memory_address(a_obj)))


def zero_day(dt, zero_hour=0):
    return dt.replace(hour=zero_hour, minute=0, second=0, microsecond=0)


def max_day(dt, zero_hour=23):
    return dt.replace(hour=zero_hour, minute=59, second=59, microsecond=0)


# TODO: this should be the first unit test
def garmin_activity_from_strava(strava_external_id):
    original = strava_external_id
    cleaned_up = original.replace('garmin_push_', '')
    return cleaned_up


def normalize_name(name_or_other, return_other=False):
    if isinstance(name_or_other, Enum):
        return name_or_other.value
    elif not isinstance(name_or_other, str):
        if return_other:
            return name_or_other
        return
    return name_or_other.strip()


def normalize_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        return int(value)
    message = f'unexpected value: {value} ' \
              f'of type: {type(value)}'
    raise NormalizeIntegerException(message)


def generate_uuid():
    return str(uuid4())


def has_query_param(incoming_request, key):
    value = incoming_request.args.get(key, None)
    return bool(value is not None)


def check_bool_query_param(incoming_request, key, returns_none=False):
    if returns_none and not has_query_param(incoming_request, key):
        return None
    value = incoming_request.args.get(key, '0')
    return bool(value == '1')


def get_version(environment='production'):
    return version

import os
from flask import current_app as app
from ..config import base_config


log = app.logger


class QNAPPinger(object):
    # FIXME: doesn't work normally because of app context
    @classmethod
    def get_metrics_interval_seconds(cls):
        # METRICS_INTERVAL_SECONDS = int(
        #     app.config.get('METRICS_INTERVAL_SECONDS'))
        # return METRICS_INTERVAL_SECONDS
        default_interval = base_config.DEFAULT_METRICS_INTERVAL_SECONDS
        return os.environ.get('METRICS_INTERVAL_SECONDS', default_interval)

    @classmethod
    def should_schedule_qnap_metrics_updates(cls):
        config_value = app.config.get("SHOULD_SCHEDULE_QNAP_METRICS_UPDATES")
        c_m = f'for SHOULD_SCHEDULE_QNAP_METRICS_UPDATES: {config_value}'
        log.debug(c_m)
        return bool(str(config_value) == "1")

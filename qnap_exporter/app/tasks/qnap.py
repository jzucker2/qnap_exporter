import os
from flask import current_app as app
from ..extensions import scheduler
from ..routers.exporter_router import ExporterRouter
from ..config import base_config


log = app.logger


# FIXME: doesn't work normally because of app context
def get_metrics_interval_seconds():
    # METRICS_INTERVAL_SECONDS = int(
    #     app.config.get('METRICS_INTERVAL_SECONDS'))
    # return METRICS_INTERVAL_SECONDS
    default_interval = base_config.DEFAULT_METRICS_INTERVAL_SECONDS
    return os.environ.get('METRICS_INTERVAL_SECONDS', default_interval)


# TODO: make this configurable and turn and off as well
@scheduler.task(
    "interval",
    id="qnap_metrics_update",
    seconds=get_metrics_interval_seconds(),
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def perform_qnap_metrics_update():
    """QNAP metrics update

    Added when app starts.
    """
    log.debug("running qnap_metrics_update!")

    with scheduler.app.app_context():
        router = ExporterRouter()
        response = router.handle_exporter_metrics_update_route_response()
        r_m = f'scheduled qnap metrics update got response: {response}'
        log.debug(r_m)

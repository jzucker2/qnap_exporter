from flask import current_app as app
from ..extensions import scheduler
from ..routers.collector_router import CollectorRouter
from .qnap_pinger import QNAPPinger


log = app.logger


# TODO: make this configurable and turn and off as well
@scheduler.task(
    "interval",
    id="qnap_metrics_update",
    seconds=QNAPPinger.get_metrics_interval_seconds(),
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def perform_qnap_metrics_update():
    """QNAP metrics update

    Added when app starts.
    """
    log.debug("running qnap_metrics_update!")

    with scheduler.app.app_context():
        router = CollectorRouter()
        response = router.handle_all_collectors_metrics_update_route_response()
        r_m = f'scheduled qnap metrics update got response: {response}'
        log.info(r_m)

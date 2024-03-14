from flask import current_app as app
from ..routers.collector_router import CollectorRouter


log = app.logger


@app.route('/api/v1/qnap/collector/simple')
def handle_simple_collector_route():
    router = CollectorRouter()
    return router.handle_simple_collector_route_response()


@app.route('/api/v1/qnap/collector/metrics/update')
def handle_collector_metrics_update_route():
    router = CollectorRouter()
    return router.handle_all_collectors_metrics_update_route_response()

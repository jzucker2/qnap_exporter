import os
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


def when_ready(server):
    # https://github.com/rycus86/prometheus_flask_exporter/blob/62e836435324501dc496059843d094c9cca909c0/examples/gunicorn/config.py
    port = int(os.getenv('METRICS_PORT'))
    GunicornPrometheusMetrics.start_http_server_when_ready(port)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


# https://docs.gunicorn.org/en/latest/configure.html
bind = "0.0.0.0:1996"
# FIXME: If this is a webserver, we can have more than 1, but we need to
#  solve for scheduler with DB and/or a semaphore. For now, avoid by
#  keeping workers limited to 1, since this is really just a
#  prometheus exporter. But in the future I could stick a dashboard on this.
workers = 1

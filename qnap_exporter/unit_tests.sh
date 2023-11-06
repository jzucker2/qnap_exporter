#!/bin/sh

export FLASK_APP=app

# https://stackoverflow.com/questions/4437573/bash-assign-default-value
: ${PROMETHEUS_MULTIPROC_DIR:=/tmp}
export PROMETHEUS_MULTIPROC_DIR
: ${prometheus_multiproc_dir:=/tmp}
export prometheus_multiproc_dir
# intended for local running on pi
: ${METRICS_PORT:=9200}
export METRICS_PORT


python -m unittest discover

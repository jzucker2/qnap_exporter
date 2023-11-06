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


echo "Set up the DB!"
echo "Going with DB_LOCATION ---> $DB_LOCATION"

# check for db first
rm app/app.db
echo "Done deleting (or checking) for /app.db"

# should probably call `set_up_db.sh` instead of copypasta
echo "First perform flask migrations"
flask db upgrade
echo "Now ensure default admin"
python ensure_admin.py

echo "Done setting up the $DB_LOCATION db!!!"

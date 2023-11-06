#!/bin/sh

gunicorn -c gunicorn.conf.py "app:create_app()"

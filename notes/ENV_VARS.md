# Env Vars

There's a bunch carried over from flask but only a few really important ones:

```
# This is optional, and will be `default` if not provided
QNAP_NAS_NAME="Plex NAS"

# this is the IP address of your QNAP
QNAP_NAS_HOST=10.0.1.1

# likely should be left to default and you don't need to provide
QNAP_PORT=8080

# this is your username
QNAP_USERNAME=harry
# this is your password (note: no 2FA supported ATM)
QNAP_PASSWORD=alohomora

# how long to wait between metrics checks
METRICS_INTERVAL_SECONDS=30

# by default, the qnap_exporter will ping the QNAP NAS at the METRICS_INTERVAL_SECONDS but to turn that off, set:
SHOULD_SCHEDULE_QNAP_METRICS_UPDATES=0

# to ensure it happens (on by default)
SHOULD_SCHEDULE_QNAP_METRICS_UPDATES=1
```

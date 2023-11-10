# Env Vars

There's a bunch carried over from flask but only a few really important ones:

```
# this is the IP address of your QNAP
QNAP_HOST_IP=10.0.1.1

# likely should be left to default and you don't need to provide
QNAP_PORT=8080

# this is your username
QNAP_USERNAME=harry
# this is your password (note: no 2FA supported ATM)
QNAP_PASSWORD=alohomora

# how long to wait between metrics checks
METRICS_INTERVAL_SECONDS=30
```

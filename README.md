# qnap_exporter

This exports metrics from a QNAP NAS for scraping by `prometheus`.

Unlike other solutions I found, this does **not** need to run on 
your actual QNAP but instead can run on any machine that has 
access to your QNAP. This greatly reduces the complexity of trying 
to run Docker (or any binary) on QTS and also reduces workload 
on the NAS.

## Installation

### Docker Compose

```
version: '3.7'

services:

  qnap_exporter:
    container_name: qnap_exporter
    image: ghcr.io/jzucker2/qnap_exporter:latest
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"
    ports:
      - "2003:2003"
      - "1805:1805"
    environment:
      - QNAP_HOST_IP=10.0.1.1
      - QNAP_USERNAME=admin
      - QNAP_PASSWORD=password
    stdin_open: true
    tty: true
```

#### Env File

If you want to use an `.env` file like in the 
root of the repo, here is an example:

```
QNAP_NAS_HOST=10.0.1.1
QNAP_NAS_USERNAME=admin
QNAP_NAS_PASSWORD=password
```

### Prometheus Config

Include this in your `prometheus.yml`

```yaml
  - job_name: 'qnap'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      # this should be the IP of `my_scraper`, can also be a DNS name.
      - targets: [ '10.0.1.10:1805' ]
        labels:
          instance: 'my_scraper'
```

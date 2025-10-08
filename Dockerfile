ARG FILMSTOCK_VERSION=0.7.9
FROM ghcr.io/jzucker2/filmstock:${FILMSTOCK_VERSION} AS linux_base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM linux_base AS python_dependencies
COPY requirements.txt requirements.txt
RUN pip wheel --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.14-slim AS base_python

RUN apt-get update -y && apt-get install -y \
        curl \
    && apt-get clean

FROM base_python AS python_installer

COPY --from=python_dependencies /app/wheels /wheels
COPY --from=python_dependencies /app/requirements.txt .

RUN pip install --no-cache /wheels/*

FROM python_installer AS source_code
COPY /qnap_exporter /qnap_exporter
WORKDIR /qnap_exporter

ENV FLASK_APP=app

FROM source_code AS app_setup
ENV PROMETHEUS_MULTIPROC_DIR=/tmp
ENV prometheus_multiproc_dir=/tmp
ENV METRICS_PORT=1805

# Expose the port on which the application will run
EXPOSE 2003
# Expose the port on which the metrics are provided
EXPOSE 1805

HEALTHCHECK --interval=5s --timeout=5s --retries=3 \
    CMD curl -f http://0.0.0.0:2003/api/v1/health || exit 1

# can use `run_dev.sh` or `run_prod.sh`
CMD ["sh", "run_prod.sh"]

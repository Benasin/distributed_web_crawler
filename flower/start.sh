#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A celery_config inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery -A celery_config  \
    --broker="redis://:redis_password@redis:6379/0" \
    flower
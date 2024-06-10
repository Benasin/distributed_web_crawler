#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="main_newsdb",
        user="main_newsuser",
        password="main_password",
        host="main_db",
        port="5432",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

worker_ready() {
    celery -A celery_config inspect ping
}

sleep 30

while true; do
    if [ $(curl -s -o /dev/null -w "%{http_code}" http://app:5000/health) -eq 200 ]; then
        echo "App is already running"
        sleep 10
        continue
    else
        echo "Server is crashed, starting the backup app"
        break
    fi
done

python run_crawler.py &
python sync_database.py &
python app.py

#!/bin/sh

# detect Ctrl+C
trap shutdown INT
shutdown() {
    celery -A demo.worker:celery control shutdown
    redis-cli shutdown
    service mysql stop
    exit
}

# activate virtual env
. ./venv/bin/activate

export FLASK_APP=demo
export FLASK_ENV=development
export HOST=$( python -c "from demo import config; print(config.HOST)" )
export PORT=$( python -c "from demo import config; print(config.PORT)" )
export WORKER=$( python -c "from demo import config; print(config.WORKER)" )
export LOG_LEVEL=warning
export LOG_DIR=log

# create log directory
mkdir -p $LOG_DIR

# start MySQL server if not running
service mysql status > /dev/null || service mysql start
# # start Redis server if not running
service redis-server status > /dev/null && service redis-server stop
redis-server --daemonize yes \
    --loglevel $LOG_LEVEL \
    --logfile $LOG_DIR/redis-server.log

# start app
celery -A demo.worker:celery worker -B \
    -l $LOG_LEVEL -f $LOG_DIR/celery.log -D \
    -s /tmp/celerybeat-schedule.db

flask init-db
gunicorn "demo:create_app()" \
    -w $WORKER -t 0 -b $HOST:$PORT \
    --log-level $LOG_LEVEL --log-file $LOG_DIR/gunicorn.log

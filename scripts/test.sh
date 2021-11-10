#!/bin/sh

export FLASK_APP=demo
export FLASK_ENV=test
export LOG_LEVEL=debug
export LOG_DIR=log

# start MySQL server if not running
service mysql status > /dev/null || service mysql start
# # start Redis server if not running
service redis-server status > /dev/null && service redis-server stop
redis-server --daemonize yes \
    --loglevel $LOG_LEVEL \
    --logfile $LOG_DIR/redis-server.log

# activate virtual env
. ./venv/bin/activate

# start test & coverage
flask init-db
python -m pytest tests/ -cov demo/ -v

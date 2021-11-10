#!/bin/sh

# check root user
if [ $(id -u) -ne 0 ]
    then echo "Please execute this script as root"
    exit
fi

# install apt packages
apt-get update
apt-get install -y -qq \
    python3 python3-dev python3-pip python3-venv python3-wheel \
    mysql-server redis-server

# venv & install python dependencies
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt

# create users & databases
service mysql start
[ -z "$SQL_USERNAME" ] && SQL_USERNAME=\
$( python3 -c "from demo import config; print(config.SQL_USERNAME)" )
[ -z "$SQL_PASSWORD" ] && SQL_PASSWORD=\
$( python3 -c "from demo import config; print(config.SQL_PASSWORD)" )
[ -z "$SQL_DATABASE" ] && SQL_DATABASE=\
$( python3 -c "from demo import config; print(config.SQL_DATABASE)" )
mysql -u "root" -e \
    "CREATE USER IF NOT EXISTS '$SQL_USERNAME'@'%' IDENTIFIED BY '$SQL_PASSWORD';"`
    `"GRANT ALL PRIVILEGES ON * . * TO '$SQL_USERNAME'@'%';"`
    `"FLUSH PRIVILEGES;"
mysql -u "root" -e "CREATE DATABASE IF NOT EXISTS $SQL_DATABASE;"
mysql -u "root" -e "CREATE DATABASE IF NOT EXISTS ${SQL_DATABASE}_test;"

# generate RSA secret key
[ -z "$JWT_SECRET_KEY_PATH" ] && JWT_SECRET_KEY_PATH=\
$(python3 -c "from demo import config; print(config.JWT_SECRET_KEY_PATH)")
[ -f $JWT_SECRET_KEY_PATH ] || openssl genrsa -out $JWT_SECRET_KEY_PATH 2048

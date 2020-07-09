#!/bin/sh -e

envsubst '$$VIRTUAL_HOST $$PHP_HOST $$PHP_PORT $$MAGE_MODE $$MAGE_ROOT $$MAGE_RUN_CODE $$MAGE_RUN_TYPE' < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf

DIR="/etc/nginx/cert/${VIRTUAL_HOST}"

echo "###############################################################"
echo "#"

if [ -d "$DIR" ]; then
  echo "#  Certificates for ${VIRTUAL_HOST} already exists."
else
  chmod -R 777 /etc/nginx/cert/ssl_generator/out
  /etc/nginx/cert/ssl_generator/create.sh ${VIRTUAL_HOST}

  echo "#  Certificates for ${VIRTUAL_HOST} just created."
fi

echo "#  Please add '0.0.0.0 ${VIRTUAL_HOST}' to '/etc/hosts' file."

echo "#"
echo "###############################################################"

echo "> $@" && exec "$@"
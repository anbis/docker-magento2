#!/bin/sh -e


if [ -d "$DIR" ]; then
  echo "#  Certificates for ${VIRTUAL_HOST} already exists."
else
  mkdir -p /etc/nginx/cert/ssl_generator/out
  chmod -R 777 /etc/nginx/cert/ssl_generator/out
  /etc/nginx/cert/ssl_generator/create.sh ${VIRTUAL_HOST}

  echo "###############################################################"
  echo "#"
  echo "#  Certificates for ${VIRTUAL_HOST} just created."
fi

echo "#  Please add '0.0.0.0 ${VIRTUAL_HOST}' to '/etc/hosts' file."

envsubst '$$VIRTUAL_HOST $$PHP_HOST $$PHP_PORT $$MAGE_MODE $$MAGE_ROOT $$MAGE_RUN_CODE $$MAGE_RUN_TYPE' < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf

echo "#"
echo "###############################################################"
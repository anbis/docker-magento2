#!/bin/bash

generate_certs() {
    echo "###############################################################"
    echo "#"

    if [ -d $3 ]; then
      echo "#"
      echo "#  Certificates for '$1' already exists."
      echo "#"
    else
      mkdir -p /etc/nginx/cert/ssl_generator/out
      chmod -R 777 /etc/nginx/cert/ssl_generator/out
      /etc/nginx/cert/ssl_generator/create.sh $1

      echo "#"
      echo "#  Certificates for '$1' just created."
      echo "#"
    fi


    echo "#  Please add '0.0.0.0 $1' to '/etc/hosts' file."
    echo "#"
    echo "#  VIRTUAL_HOST = $1"
    echo "#  MAGE_RUN_CODE = $2"
    echo "#  MAGE_RUN_TYPE = $MAGE_RUN_TYPE"
    echo "#"
    echo "#"
    echo "###############################################################"
}

rm -rf /etc/nginx/conf.d/subdomains/*

envsubst '$$PHP_HOST $$PHP_PORT $$PHP_HOST_XDEBUG $$PHP_PORT_XDEBUG' < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf

generate_certs ${VIRTUAL_HOST} ${MAGE_RUN_CODE} /etc/nginx/cert/${VIRTUAL_HOST}
envsubst '$$VIRTUAL_HOST $$PHP_HOST $$PHP_PORT $$MAGE_MODE $$MAGE_ROOT $$MAGE_RUN_CODE $$MAGE_RUN_TYPE' < /etc/nginx/conf.d/subdomain.template > /etc/nginx/conf.d/subdomains/${VIRTUAL_HOST}.conf

for string in $DOMAINS
do
    set -f
    array=(${string//=/ })
    for i in "${!array[@]}"
    do
        if [ $i == 0 ]
        then
            VIRTUAL_HOST=${array[i]}
        else
            MAGE_RUN_CODE=${array[i]}
        fi
    done

    generate_certs ${VIRTUAL_HOST} ${MAGE_RUN_CODE} /etc/nginx/cert/${VIRTUAL_HOST}
    envsubst '$$VIRTUAL_HOST $$PHP_HOST $$PHP_PORT $$MAGE_MODE $$MAGE_ROOT $$MAGE_RUN_CODE $$MAGE_RUN_TYPE' < /etc/nginx/conf.d/subdomain.template > /etc/nginx/conf.d/subdomains/${VIRTUAL_HOST}.conf
done
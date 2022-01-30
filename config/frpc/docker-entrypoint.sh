#!/bin/sh

echo ${INTERNET_HOST}

sed -e "s/INTERNET_HOST/${INTERNET_HOST}/g" /etc/frp/frpc.template > /etc/frp/frpc.ini

/usr/bin/frpc -c /etc/frp/frpc.ini
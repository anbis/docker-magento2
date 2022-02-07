#!/bin/sh

echo "###############################################################"
echo "#"
echo "#"
echo "#  Your local environment available as '${INTERNET_HOST}' at Internet."
echo "#"
echo "#"
echo "###############################################################"

sed -e "s/INTERNET_HOST/${INTERNET_HOST}/g" /etc/frp/frpc.template > /etc/frp/frpc.ini

/usr/bin/frpc -c /etc/frp/frpc.ini
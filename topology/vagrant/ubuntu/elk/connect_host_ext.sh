#!/bin/sh
echo $1
var=$(echo $1 | python3 /home/vagrant/take_ip.py)
echo $var

echo "REDIRECT TO COWRIE SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$var\", \"Dpid\": \"85884017520972\"}" \
   http://192.168.11.100:8080/rest_controller/push_dmz_server_out

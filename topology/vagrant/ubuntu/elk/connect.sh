#!/bin/sh
echo $1
echo "REDIRECT TO COWRIE SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\"}" \
   http://192.168.5.100:8080/rest_controller/redirect_ssh_int

echo "REDIRECT TO HERALDING"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\"}" \
   http://192.168.5.100:8080/rest_controller/redirect_to_heralding

echo "REDIRECT TO COWRIE SMTP TELNET"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\"}" \
   http://192.168.5.100:8080/rest_controller/redirect_to_cowrie_telnet

echo "REDIRECT TO COWRIE HTTP PORT HOPPING"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"85884017520972\"}" \
   http://192.168.5.100:8080/rest_controller/http_port_hopping


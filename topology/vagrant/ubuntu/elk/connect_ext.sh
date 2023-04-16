#!/bin/sh
echo $1
echo "REDIRECT TO HERALDING DMZ SSH"
curl -X POST \
   -H 'Content-Type: application/json' \
   -d "{\"Source_IP\": \"$1\", \"Dpid\": \"101737510984148\"}" \
   http://192.168.11.100:8080/rest_controller/redirect_ssh_dmz


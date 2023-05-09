#!/bin/sh

sudo apt update

# vedi servizio vulnerabile da installare

#auditbeat
curl -L -O https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-8.7.0-amd64.deb
sudo dpkg -i auditbeat-8.7.0-amd64.deb

sudo cp /home/emma/ubuntu/dmz_service/auditbeat.yml /etc/auditbeat/auditbeat.yml
sudo service auditbeat start
sudo systemctl enable auditbeat

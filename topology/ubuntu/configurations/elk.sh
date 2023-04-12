#!/usr/bin/env bash

set -efux

sudo hostnamectl set-hostname 'elk'

sudo sed -i 's/#Port 22/Port 40002/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd

sudo apt-get update
sudo apt-get install -y openjdk-8-jdk

sudo apt-get update
sudo apt-get install -y apt-transport-https

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.0-amd64.deb
sudo dpkg -i elasticsearch-7.9.0-amd64.deb

wget https://artifacts.elastic.co/downloads/logstash/logstash-7.9.0.deb
sudo dpkg -i logstash-7.9.0.deb

wget https://artifacts.elastic.co/downloads/kibana/kibana-7.9.0-amd64.deb
sudo dpkg -i kibana-7.9.0-amd64.deb

sudo su<<EOF
cp /home/emma/ubuntu/elk/kibana.yml /etc/kibana/
EOF

sudo service elasticsearch start
sudo service kibana start
sudo systemctl enable kibana
sudo systemctl enable elasticsearch.service

sudo su<<EOF
cp /home/emma/ubuntu/elk/logstash.conf /etc/logstash/
EOF

sudo service logstash start
sudo systemctl enable logstash

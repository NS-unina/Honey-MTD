#!/usr/bin/env bash

set -efux

sudo hostnamectl set-hostname 'dmz-heralding'

sudo apt-get update
export PATH=$PATH:/home/ubuntu/.local/bin

sudo sed -i 's/#Port 22/Port 40006/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd

sudo apt-get -y install net-tools

sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt-get -y update
sudo apt-get install -y python3.8 python3.8-dev python3-pip python3-virtualenv
sudo apt-get install -y build-essential libssl-dev libffi-dev libpq-dev
virtualenv --python=python3.8 heralding
source heralding/bin/activate
pip3 install heralding
cp /home/emma/ubuntu/dmz_heralding/heralding.yml /home/vagrant/heralding/lib/python3.8/site-packages/heralding/heralding.yml
#nohup heralding &
cp /home/emma/ubuntu/dmz_heralding/conf.sh /home/vagrant
cp /home/emma/ubuntu/dmz_heralding/start.sh /home/vagrant


curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.7.0-amd64.deb
sudo dpkg -i filebeat-8.7.0-amd64.deb

curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-8.7.0-amd64.deb
sudo dpkg -i metricbeat-8.7.0-amd64.deb

sudo cp /home/emma/ubuntu/dmz_heralding/metricbeat.yml /etc/metricbeat/metricbeat.yml
sudo service metricbeat start
sudo systemctl enable metricbeat


sudo cp /home/emma/ubuntu/dmz_heralding/filebeat.yml /etc/filebeat/filebeat.yml
sudo service filebeat start
sudo systemctl enable filebeat

#!/bin/sh

cd /home/vagrant/elastalert
elastalert-create-index
python3 -m elastalert.elastalert --verbose &

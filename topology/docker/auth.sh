#!/bin/bash

sudo docker exec int_host /home/conf.sh
sudo docker exec ext_host /home/conf.sh
sudo docker exec ssh_server /home/conf.sh
sudo docker exec controller /home/conf.sh
sudo docker exec int_ssh_server /home/conf.sh
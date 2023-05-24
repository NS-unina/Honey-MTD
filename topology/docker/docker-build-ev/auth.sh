#!/bin/bash

for i in `seq 1 30`;
do
    sudo docker exec docker-build-ev-int_ssh_server-$i /home/conf.sh
done  

sudo docker exec int_host /home/conf.sh
sudo docker exec ext_host /home/conf.sh
sudo docker exec ssh_server /home/conf.sh
sudo docker exec controller /home/conf.sh
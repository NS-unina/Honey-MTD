#!/bin/bash

for i in `seq 1 20`;
do
    sudo docker exec docker-build-ev2-int_ssh_server-$i /home/conf.sh
done  

sudo docker exec int_host /home/conf.sh
sudo docker exec ext_host /home/conf.sh
sudo docker exec ssh_server /home/conf.sh
sudo docker exec controller /home/conf.sh
#!/bin/bash
for i in `seq 1 10`;
do
    sudo docker exec docker-build-ev-int_ssh_server-$i /home/conf.sh
done  
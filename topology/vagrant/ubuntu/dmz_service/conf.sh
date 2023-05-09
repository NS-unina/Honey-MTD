#!/bin/sh

sudo ip route add 192.168.4.0/24 via 192.168.3.1 dev eth1
sudo ip route add 192.168.5.0/24 via 192.168.3.1 dev eth1
sudo ip route add 192.168.10.0/24 via 192.168.3.1 dev eth1
sudo ip route add 192.168.11.0/24 via 192.168.3.1 dev eth1

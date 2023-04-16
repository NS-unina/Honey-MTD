#!/bin/sh

sudo ip route add 192.168.3.0/24 via 192.168.4.1 dev enp0s8
sudo ip route add 192.168.5.0/24 via 192.168.4.1 dev enp0s8
sudo ip route add 192.168.10.0/24 via 192.168.4.1 dev enp0s8
sudo ip route add 192.168.11.0/24 via 192.168.4.1 dev enp0s8



#!/bin/sh

ip route add 192.168.11.0/24 via 192.168.4.1 dev enp0s8
ip route add 192.168.4.0/24 via 192.168.5.1 dev enp0s8
ip route add 192.168.10.0/24 via 192.168.11.1 dev enp0s9

#!/bin/sh

ip route add 192.168.10.0/24 via 192.168.11.1 dev eth2
ip route add 192.168.3.0/24 via 192.168.5.1 dev eth1
ip route add 192.168.4.0/24 via 192.168.5.1 dev eth1
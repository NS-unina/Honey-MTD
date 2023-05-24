#!/bin/sh

ip route add 192.168.11.0/24 via 192.168.10.1 dev eth1
ip route add 192.168.3.0/24 via 192.168.10.1 dev eth1
ip route add 192.168.4.0/24 via 192.168.10.1 dev eth1
ip route add 192.168.5.0/24 via 192.168.10.1 dev eth1
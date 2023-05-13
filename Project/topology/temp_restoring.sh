#!/bin/sh

if sudo ovs-ofctl show br1 | grep -q "(wlp0s20f3)"; then
   sudo ovs-vsctl del-port wlp0s20f3
fi

sudo netplan apply

sleep 10

sudo ifconfig wlp0s20f3 192.168.92.106/24 up
sudo route del default gw 192.168.92.68 br1
sudo route add default gw 192.168.92.68 wlp0s20f3
sudo sed -i '1s/^/nameserver 8.8.8.8\n/' /etc/resolv.conf


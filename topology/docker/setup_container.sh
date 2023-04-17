#!/bin/sh


sudo ./my-ovs-docker del-port br0 eth1 controller
sudo ./my-ovs-docker del-port br1 eth2 controller
sudo docker stop controller
sudo docker start controller
sudo ./my-ovs-docker add-port br0 eth1 controller c1 20 --ipaddress=192.168.5.100/24
sudo ovs-vsctl -- set port c1_l tag=3
sudo iptables -t nat -A POSTROUTING -o c1_l -j MASQUERADE
sudo ./my-ovs-docker add-port br1 eth2 controller c2 21 --ipaddress=192.168.11.100/24
sudo ovs-vsctl -- set port c2_l tag=11
sudo iptables -t nat -A POSTROUTING -o c2_l -j MASQUERADE

sudo ./my-ovs-docker del-port br0 eth1 int_host
sudo docker stop int_host
sudo docker start int_host
sudo ./my-ovs-docker add-port br0 eth1 int_host h1 15 --ipaddress=192.168.3.10/24 --macaddress=08:00:27:b6:d0:66
sudo ovs-vsctl -- set port h1_l tag=1
sudo iptables -t nat -A POSTROUTING -o h1_l -j MASQUERADE

sudo ./my-ovs-docker del-port br1 eth1 ssh_server
sudo docker stop ssh_server
sudo docker start ssh_server
sudo ./my-ovs-docker add-port br1 eth1 ssh_server s1 22 --ipaddress=192.168.10.11/24 --macaddress=08:00:27:b6:d0:67
sudo ovs-vsctl -- set port s1_l tag=10
sudo iptables -t nat -A POSTROUTING -o s1_l -j MASQUERADE

sudo ./my-ovs-docker del-port br1 eth1 ext_host
sudo docker stop ext_host
sudo docker start ext_host
sudo ./my-ovs-docker add-port br1 eth1 ext_host h2 23 --ipaddress=192.168.10.12/24 --macaddress=08:00:27:b6:d0:68
sudo ovs-vsctl -- set port h2_l tag=10
sudo iptables -t nat -A POSTROUTING -o h2_l -j MASQUERADE
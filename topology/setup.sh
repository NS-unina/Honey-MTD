#!/bin/sh

echo "Restoring Network ..."
sudo ovs-vsctl del-port wlo1
sudo netplan apply
sleep 10
sudo ovs-vsctl del-port tap1
sudo ip tuntap add name tap1 mode tap
sudo ip link set tap1 up
sudo ovs-vsctl add-port br0 tap1 tag=1 -- set interface tap1 ofport=2
sudo ovs-vsctl del-port tap2
sudo ip tuntap add name tap2 mode tap
sudo ip link set tap2 up
sudo ovs-vsctl add-port br0 tap2 tag=1 -- set interface tap2 ofport=3
sudo ovs-vsctl del-port tap3
sudo ip tuntap add name tap3 mode tap
sudo ip link set tap3 up
sudo ovs-vsctl add-port br0 tap3 tag=1 -- set interface tap3 ofport=4
sudo ovs-vsctl del-port tap4
sudo ip tuntap add name tap4 mode tap
sudo ip link set tap4 up
sudo ovs-vsctl add-port br0 tap4 tag=2 -- set interface tap4 ofport=6
sudo ovs-vsctl del-port tap7
sudo ip tuntap add name tap7 mode tap
sudo ip link set tap7 up
sudo ovs-vsctl add-port br0 tap7 tag=2 -- set interface tap7 ofport=13
sudo ovs-vsctl del-port tap5
sudo ip tuntap add name tap5 mode tap
sudo ip link set tap5 up
sudo ovs-vsctl add-port br0 tap5 tag=3 -- set interface tap5 ofport=8
sudo ovs-vsctl del-port tap6
sudo ip tuntap add name tap6 mode tap
sudo ip link set tap6 up
sudo ovs-vsctl add-port br0 tap6 tag=3 -- set interface tap6 ofport=9

sudo ovs-vsctl del-port br1 tap10
sudo ip tuntap add name tap10 mode tap
sudo ip link set tap10 up
sudo ovs-vsctl add-port br1 tap10 tag=10 -- set interface tap10 ofport=2
sudo ovs-vsctl del-port br1 tap11
sudo ip tuntap add name tap11 mode tap
sudo ip link set tap11 up
sudo ovs-vsctl add-port br1 tap11 tag=11 -- set interface tap11 ofport=13

sudo sudo ifconfig vlan1 192.168.3.1/24 up
sudo sudo ifconfig vlan2 192.168.4.1/24 up
sudo sudo ifconfig vlan3 192.168.5.1/24 up
sudo sudo ifconfig vlan10 192.168.10.1/24 up
sudo sudo ifconfig vlan11 192.168.11.1/24 up


sudo iptables -t nat -A POSTROUTING -o vlan1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o vlan2 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o vlan3 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o vlan10 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o vlan11 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap2 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap3 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap4 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap5 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap6 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap10 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o tap11 -j MASQUERADE

sleep 5
sudo ovs-vsctl add-port br1 wlo1 -- set interface wlo1 ofport=10
sudo ifconfig wlo1 0
#sudo ifconfig br1 192.168.244.95/24 up
#sudo route add default gw 192.168.244.139 br1

sudo ifconfig br1 192.168.1.16/24 up
sudo route add default gw 192.168.1.1 br1
sudo iptables -t nat -A POSTROUTING -o br1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE
sudo sed -i '1s/^/nameserver 8.8.8.8\n/' /etc/resolv.conf

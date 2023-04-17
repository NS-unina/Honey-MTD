#!/bin/sh

sudo ovs-vsctl del-br br0
sudo ovs-vsctl del-br br1
sleep 10

echo "Start Network setup ..."
echo "Enable IP forwarding"
sudo sysctl -w net.ipv4.ip_forward=1
echo "OVS setup"
sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-br br1

echo "Subnet1: IP 192.168.3.0/24"
sudo ovs-vsctl add-port br0 vlan1 -- set interface vlan1 type=internal ofport=1
sudo ovs-vsctl set port vlan1 tag=1
sudo ifconfig vlan1 192.168.3.1/24 up
sudo iptables -t nat -A POSTROUTING -o vlan1 -j MASQUERADE

echo "Subnet2: IP 192.168.4.0/24"
sudo ovs-vsctl add-port br0 vlan2 -- set interface vlan2 type=internal ofport=5
sudo ovs-vsctl set port vlan2 tag=2
sudo ifconfig vlan2 192.168.4.1/24 up
sudo iptables -t nat -A POSTROUTING -o vlan2 -j MASQUERADE

echo "Subnet3: IP 192.168.5.0/24"
sudo ovs-vsctl add-port br0 vlan3 -- set interface vlan3 type=internal ofport=7
sudo ovs-vsctl set port vlan3 tag=3
sudo ifconfig vlan3 192.168.5.1/24 up
sudo iptables -t nat -A POSTROUTING -o vlan3 -j MASQUERADE

echo "Connect br0 to controller 192.168.5.100:6633"
sudo ovs-vsctl set-controller br0 tcp:192.168.5.100:6633

echo "Subnet10: IP 192.168.10.0/24"
sudo ovs-vsctl add-port br1 vlan10 -- set interface vlan10 type=internal ofport=1
sudo ovs-vsctl set port vlan10 tag=10
sudo ifconfig vlan1 192.168.10.1/24 up
sudo iptables -t nat -A POSTROUTING -o vlan10 -j MASQUERADE

echo "Subnet11: IP 192.168.11.0/24"
sudo ovs-vsctl add-port br1 vlan11 -- set interface vlan11 type=internal ofport=4
sudo ovs-vsctl set port vlan10 tag=11
sudo ifconfig vlan1 192.168.11.1/24 up
sudo iptables -t nat -A POSTROUTING -o vlan11 -j MASQUERADE

echo "Connect br1 to controller 192.168.11.100:6633"
sudo ovs-vsctl set-controller br1 tcp:192.168.11.100:6633

#!/bin/sh

if sudo ovs-vsctl show | grep -q "Bridge br0"; then
   sudo ovs-vsctl del-br br0
fi

if sudo ovs-vsctl show | grep -q "Bridge br1"; then
   sudo ovs-vsctl del-br br1
fi
sleep 10

echo "Start Network setup ..."
echo "Enable IP forwarding"
sudo sysctl -w net.ipv4.ip_forward=1
echo "OVS setup"
sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-br br1
sudo ovs-vsctl set bridge br0 other_config:hwaddr=3a:4d:a7:05:2a:45
sudo ovs-vsctl set bridge br1 other_config:hwaddr=3a:4d:a7:05:2a:46

# sudo ovs-vsctl set bridge br0 other-config:datapath-id=209326269119040
# sudo ovs-vsctl set bridge br1 other-config:datapath-id=187971798259276

#209544804549707
#33227011233353

echo "Subnet1: IP 192.168.3.0/24"
sudo ovs-vsctl add-port br0 vlan1 -- set interface vlan1 type=internal ofport=1
sudo ovs-vsctl set port vlan1 tag=1
sudo ifconfig vlan1 192.168.3.1/24 up
sudo ifconfig vlan1 hw ether 9e:c3:c6:49:0e:e8
sudo iptables -t nat -A POSTROUTING -o vlan1 -j MASQUERADE

echo "Subnet2: IP 192.168.4.0/24"
sudo ovs-vsctl add-port br0 vlan2 -- set interface vlan2 type=internal ofport=5
sudo ovs-vsctl set port vlan2 tag=2
sudo ifconfig vlan2 192.168.4.1/24 up
sudo ifconfig vlan2 hw ether 16:67:1f:3f:86:a7
sudo iptables -t nat -A POSTROUTING -o vlan2 -j MASQUERADE

echo "Subnet3: IP 192.168.5.0/24"
sudo ovs-vsctl add-port br0 vlan3 -- set interface vlan3 type=internal ofport=7
sudo ovs-vsctl set port vlan3 tag=3
sudo ifconfig vlan3 192.168.5.1/24 up
sudo ifconfig vlan3 hw ether fe:46:67:35:0d:d1
sudo iptables -t nat -A POSTROUTING -o vlan3 -j MASQUERADE

echo "Connect br0 to controller 192.168.5.100:6633"
sudo ovs-vsctl set-controller br0 tcp:192.168.5.100:6633

echo "Subnet10: IP 192.168.10.0/24"
sudo ovs-vsctl add-port br1 vlan10 -- set interface vlan10 type=internal ofport=40
sudo ovs-vsctl set port vlan10 tag=10
sudo ifconfig vlan10 192.168.10.1/24 up
sudo ifconfig vlan10 hw ether 8a:ae:02:40:8f:93
sudo iptables -t nat -A POSTROUTING -o vlan10 -j MASQUERADE

echo "Subnet11: IP 192.168.11.0/24"
sudo ovs-vsctl add-port br1 vlan11 -- set interface vlan11 type=internal ofport=41
sudo ovs-vsctl set port vlan11 tag=11
sudo ifconfig vlan11 192.168.11.1/24 up
sudo ifconfig vlan11 hw ether ea:6a:20:a0:96:11
sudo iptables -t nat -A POSTROUTING -o vlan11 -j MASQUERADE

echo "Connect br1 to controller 192.168.11.100:6633"
sudo ovs-vsctl set-controller br1 tcp:192.168.11.100:6633

sudo iptables -A FORWARD -i vlan1 -o vlan2 -j ACCEPT
sudo iptables -A FORWARD -i vlan2 -o vlan1 -j ACCEPT
sudo iptables -A FORWARD -i vlan1 -o vlan3 -j ACCEPT
sudo iptables -A FORWARD -i vlan3 -o vlan1 -j ACCEPT
sudo iptables -A FORWARD -i vlan1 -o vlan10 -j ACCEPT
sudo iptables -A FORWARD -i vlan10 -o vlan1 -j ACCEPT
sudo iptables -A FORWARD -i vlan1 -o vlan11 -j ACCEPT
sudo iptables -A FORWARD -i vlan11 -o vlan1 -j ACCEPT
sudo iptables -A FORWARD -i vlan2 -o vlan3 -j ACCEPT
sudo iptables -A FORWARD -i vlan3 -o vlan2 -j ACCEPT
sudo iptables -A FORWARD -i vlan2 -o vlan10 -j ACCEPT
sudo iptables -A FORWARD -i vlan10 -o vlan2 -j ACCEPT
sudo iptables -A FORWARD -i vlan2 -o vlan11 -j ACCEPT
sudo iptables -A FORWARD -i vlan11 -o vlan2 -j ACCEPT
sudo iptables -A FORWARD -i vlan3 -o vlan10 -j ACCEPT
sudo iptables -A FORWARD -i vlan10 -o vlan3 -j ACCEPT
sudo iptables -A FORWARD -i vlan3 -o vlan11 -j ACCEPT
sudo iptables -A FORWARD -i vlan11 -o vlan3 -j ACCEPT
sudo iptables -A FORWARD -i vlan11 -o vlan10 -j ACCEPT
sudo iptables -A FORWARD -i vlan10 -o vlan11 -j ACCEPT

sudo ovs-vsctl -- add-port br0 patch0 -- set interface patch0 type=patch ofport=45 options:peer=patch1 \
-- add-port br1 patch1 -- set interface patch1 type=patch ofport=46 options:peer=patch0

sudo iptables -t nat -A POSTROUTING -o patch0 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o patch1 -j MASQUERADE


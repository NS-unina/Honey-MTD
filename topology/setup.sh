#!/bin/sh

echo "Restoring Network ..."

if sudo ovs-ofctl show br0 | grep -q "(tap1)"; then
   sudo ovs-vsctl del-port tap1
fi

if ip a | grep -q "tap1:." | grep -q "state UP"; then
   :
elif ip a | grep "tap1:"| grep -q "state DOWN"; then
   sudo ip link set tap1 up
   sudo ovs-vsctl add-port br0 tap1 tag=1 -- set interface tap1 ofport=2
else
   sudo ip tuntap add name tap1 mode tap
   sudo ip link set tap1 up
   sudo ovs-vsctl add-port br0 tap1 tag=1 -- set interface tap1 ofport=2
fi



if sudo ovs-ofctl show br0 | grep -q "(tap2)"; then
   sudo ovs-vsctl del-port tap2
fi

if ip a | grep -q "tap2:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap2:." | grep -q "state DOWN"; then
   sudo ip link set tap2 up
   sudo ovs-vsctl add-port br0 tap2 tag=1 -- set interface tap2 ofport=3
else
   sudo ip tuntap add name tap2 mode tap
   sudo ip link set tap2 up
   sudo ovs-vsctl add-port br0 tap2 tag=1 -- set interface tap2 ofport=3
fi



if sudo ovs-ofctl show br0 | grep -q "(tap3)"; then
   sudo ovs-vsctl del-port tap3
fi

if ip a | grep -q "tap3:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap3:." | grep -q "state DOWN"; then
   sudo ip link set tap3 up
   sudo ovs-vsctl add-port br0 tap3 tag=1 -- set interface tap3 ofport=4
else
   sudo ip tuntap add name tap3 mode tap
   sudo ip link set tap3 up
   sudo ovs-vsctl add-port br0 tap3 tag=1 -- set interface tap3 ofport=4
fi



if sudo ovs-ofctl show br0 | grep -q "(tap4)"; then
   sudo ovs-vsctl del-port tap4
fi

if ip a | grep -q "tap4:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap4:." | grep -q "state DOWN"; then
   sudo ip link set tap4 up
   sudo ovs-vsctl add-port br0 tap4 tag=2 -- set interface tap4 ofport=6
else
   sudo ip tuntap add name tap4 mode tap
   sudo ip link set tap4 up
   sudo ovs-vsctl add-port br0 tap4 tag=2 -- set interface tap4 ofport=6
fi



if sudo ovs-ofctl show br0 | grep -q "(tap7)"; then
   sudo ovs-vsctl del-port tap7
fi

if ip a | grep -q "tap7:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap7:." | grep -q "state DOWN"; then
   sudo ip link set tap7 up
   sudo ovs-vsctl add-port br0 tap7 tag=2 -- set interface tap7 ofport=13
else
   sudo ip tuntap add name tap7 mode tap
   sudo ip link set tap7 up
   sudo ovs-vsctl add-port br0 tap7 tag=2 -- set interface tap7 ofport=13
fi



if sudo ovs-ofctl show br0 | grep -q "(tap5)"; then
   sudo ovs-vsctl del-port tap5
fi

if ip a | grep -q "tap5:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap5:." | grep -q "state DOWN"; then
   sudo ip link set tap5 up
   sudo ovs-vsctl add-port br0 tap5 tag=3 -- set interface tap5 ofport=8
else
   sudo ip tuntap add name tap5 mode tap
   sudo ip link set tap5 up
   sudo ovs-vsctl add-port br0 tap5 tag=3 -- set interface tap5 ofport=8
fi



if sudo ovs-ofctl show br0 | grep -q "(tap6)"; then
   sudo ovs-vsctl del-port tap6
fi

if ip a | grep -q "tap6:." | grep -q "state UP"; then
   :
elif ip a | grep -q "tap6:." | grep -q "state DOWN"; then
   sudo ip link set tap6 up
   sudo ovs-vsctl add-port br0 tap6 tag=3 -- set interface tap6 ofport=9
else
   sudo ip tuntap add name tap6 mode tap
   sudo ip link set tap6 up
   sudo ovs-vsctl add-port br0 tap6 tag=3 -- set interface tap6 ofport=9
fi


if sudo ovs-ofctl show br1 | grep -q "(tap10)"; then
   sudo ovs-vsctl del-port tap10
fi

if ip a | grep -q "tap10:." | grep "state UP"; then
   :
elif ip a | grep -q "tap10:." | grep "state DOWN"; then
   sudo ip link set tap10 up
   sudo ovs-vsctl add-port br1 tap10 tag=10 -- set interface tap10 ofport=2
else
   sudo ip tuntap add name tap10 mode tap
   sudo ip link set tap10 up
   sudo ovs-vsctl add-port br1 tap10 tag=10 -- set interface tap10 ofport=2
fi



if sudo ovs-ofctl show br1 | grep -q "(tap11)"; then
   sudo ovs-vsctl del-port tap11
fi

if ip a | grep -q "tap11:." | grep "state UP"; then
   :
elif ip a | grep -q "tap11:." | grep "state DOWN"; then
   sudo ip link set tap11 up
   sudo ovs-vsctl add-port br1 tap11 tag=11 -- set interface tap11 ofport=13
else
   sudo ip tuntap add name tap11 mode tap
   sudo ip link set tap11 up
   sudo ovs-vsctl add-port br1 tap11 tag=11 -- set interface tap11 ofport=13
fi

if ifconfig | grep -q -A2 "vlan1:*" | grep -q "inet "; then
   :
else
   sudo sudo ifconfig vlan1 192.168.3.1/24 up
   sudo ifconfig vlan1 hw ether 9e:c3:c6:49:0e:e8
fi

if ifconfig | grep -q -A2 "vlan2:*" | grep -q "inet "; then
   :
else
   sudo sudo ifconfig vlan2 192.168.4.1/24 up
   sudo ifconfig vlan2 hw ether 16:67:1f:3f:86:a7
fi

if ifconfig | grep -q -A2 "vlan3:*" | grep -q "inet "; then
   :
else
   sudo sudo ifconfig vlan3 192.168.5.1/24 up
   sudo ifconfig vlan3 hw ether fe:46:67:35:0d:d1
fi

if ifconfig | grep -q -A2 "vlan10:*" | grep -q "inet "; then
   :
else
   sudo sudo ifconfig vlan10 192.168.10.1/24 up
   sudo ifconfig vlan10 hw ether 8a:ae:02:40:8f:93
fi

if ifconfig | grep -q -A2 "vlan11:*" | grep -q "inet "; then
   :
else
   sudo sudo ifconfig vlan11 192.168.11.1/24 up
   sudo ifconfig vlan11 hw ether ea:6a:20:a0:96:11
fi

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

sleep 5
if sudo ovs-ofctl show br1 | grep -q "(wlp0s20f3)"; then
   sudo ovs-vsctl del-port wlp0s20f3
fi
sudo ovs-vsctl add-port br1 wlp0s20f3 -- set interface wlp0s20f3 ofport=10
sudo ifconfig wlp0s20f3 0
sudo ifconfig br1 192.168.92.106/24 up
sudo route add default gw 192.168.92.68 br1

#sudo ifconfig br1 192.168.1.16/24 up
#sudo route add default gw 192.168.1.1 br1
sudo iptables -t nat -A POSTROUTING -o br1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o wlp0s20f3 -j MASQUERADE
sudo sed -i '1s/^/nameserver 8.8.8.8\n/' /etc/resolv.conf

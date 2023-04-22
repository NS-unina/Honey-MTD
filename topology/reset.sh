#!/bin/sh

if sudo ovs-vsctl show | grep -q "Bridge br0"; then
   sudo ovs-vsctl del-br br0
fi

if sudo ovs-vsctl show | grep -q "Bridge br1"; then
   sudo ovs-vsctl del-br br1
fi

if ip a | grep -q "tap1:."; then
   sudo ip link delete tap1
fi

if ip a | grep -q "tap2:."; then
   sudo ip link delete tap2
fi

if ip a | grep -q "tap3:."; then
   sudo ip link delete tap3
fi

if ip a | grep -q "tap4:."; then
   sudo ip link delete tap4
fi

if ip a | grep -q "tap5:."; then
   sudo ip link delete tap5
fi

if ip a | grep -q "tap6:."; then
   sudo ip link delete tap6
fi

if ip a | grep -q "tap7:."; then
   sudo ip link delete tap7
fi

if ip a | grep -q "tap10:."; then
   sudo ip link delete tap10
fi

if ip a | grep -q "tap11:."; then
   sudo ip link delete tap11
fi

if ip a | grep -q "c1_l@"; then
   sudo ip link delete c1_l
fi

if ip a | grep -q "c2_l@"; then
   sudo ip link delete c2_l
fi

if ip a | grep -q "h1_l@"; then
   sudo ip link delete h1_l
fi

if ip a | grep -q "h2_l@"; then
   sudo ip link delete h2_l
fi

if ip a | grep -q "s1_l@"; then
   sudo ip link delete s1_l
fi

sudo netplan apply

if ifconfig | grep -q -A2 "wlp0s20f3:*" | grep -q "inet "; then
   echo "wlp0s20f3 still exists"
else
   sudo ifconfig wlp0s20f3 192.168.92.106/24 up
   sudo route add default gw 192.168.92.68 wlp0s20f3
fi
sleep 5

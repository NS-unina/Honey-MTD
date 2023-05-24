#!/bin/sh

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller \
   external_ids:container_iface=eth1 | grep -q "c1_l"; then
        sudo ./my-ovs-docker del-port br0 eth1 controller
fi

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=controller \
   external_ids:container_iface=eth2 | grep -q "c2_l"; then
        sudo ./my-ovs-docker del-port br1 eth2 controller
fi

# Remember to change containers name if they change
sudo docker stop controller
sudo docker start controller

sudo ./my-ovs-docker add-port br0 eth1 controller c1 20 --ipaddress=192.168.5.100/24
sudo ovs-vsctl -- set port c1_l tag=3
sudo iptables -t nat -A POSTROUTING -o c1_l -j MASQUERADE
sudo ./my-ovs-docker add-port br1 eth2 controller c2 21 --ipaddress=192.168.11.100/24
sudo ovs-vsctl -- set port c2_l tag=11
sudo iptables -t nat -A POSTROUTING -o c2_l -j MASQUERADE

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_host \
   external_ids:container_iface=eth1 | grep -q "h1_l"; then
        sudo ./my-ovs-docker del-port br0 eth1 int_host
fi

sudo docker stop int_host
sudo docker start int_host

sudo ./my-ovs-docker add-port br0 eth1 int_host h1 15 --ipaddress=192.168.3.10/24 --macaddress=08:00:27:b6:d0:66
sudo ovs-vsctl -- set port h1_l tag=1
sudo iptables -t nat -A POSTROUTING -o h1_l -j MASQUERADE



# if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=int_ssh_server \
#    external_ids:container_iface=eth1 | grep -q "h3_l"; then
#         sudo ./my-ovs-docker del-port br0 eth1 int_ssh_server
# fi

# sudo docker stop int_ssh_server
# sudo docker start int_ssh_server

# sudo ./my-ovs-docker add-port br0 eth1 int_ssh_server h3 16 --ipaddress=192.168.3.13/24 --macaddress=08:00:27:b6:d0:69
# sudo ovs-vsctl -- set port h3_l tag=1
# sudo iptables -t nat -A POSTROUTING -o h3_l -j MASQUERADE




if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=ssh_server \
   external_ids:container_iface=eth1 | grep -q "s1_l"; then
        sudo ./my-ovs-docker del-port br1 eth1 ssh_server
fi

sudo docker stop ssh_server
sudo docker start ssh_server

sudo ./my-ovs-docker add-port br1 eth1 ssh_server s1 22 --ipaddress=192.168.10.11/24 --macaddress=08:00:27:b6:d0:67
sudo ovs-vsctl -- set port s1_l tag=10
sudo iptables -t nat -A POSTROUTING -o s1_l -j MASQUERADE

if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=ext_host \
   external_ids:container_iface=eth1 | grep -q "h2_l"; then
        sudo ./my-ovs-docker del-port br1 eth1 ext_host
fi

sudo docker stop ext_host
sudo docker start ext_host

sudo ./my-ovs-docker add-port br1 eth1 ext_host h2 23 --ipaddress=192.168.10.12/24 --macaddress=08:00:27:b6:d0:68
sudo ovs-vsctl -- set port h2_l tag=10
sudo iptables -t nat -A POSTROUTING -o h2_l -j MASQUERADE
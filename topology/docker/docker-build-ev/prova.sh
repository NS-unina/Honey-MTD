#!/bin/bash

IP_array=(192.168.3.13/24
192.168.3.14/24
192.168.3.15/24
192.168.3.16/24
192.168.3.17/24
192.168.3.18/24
192.168.3.19/24
192.168.3.20/24
192.168.3.21/24
192.168.3.22/24)

MAC_array=(08:00:27:b6:d0:69
08:00:27:b6:d0:70
08:00:27:b6:d0:71
08:00:27:b6:d0:72
08:00:27:b6:d0:73
08:00:27:b6:d0:74
08:00:27:b6:d0:75
08:00:27:b6:d0:76
08:00:27:b6:d0:77
08:00:27:b6:d0:78)


PORT_array=(26
27
28
29
30
31
32
33
34
35)


PORT_NAME_array=("h3"
"h4"
"h5"
"h6"
"h7"
"h8"
"h9"
"h10"
"h11"
"h12")


for i in ${!IP_array[@]}; do
  echo "element $i is ${IP_array[$i]}, ${MAC_array[$i]}, ${PORT_array[$i]}, ${PORT_NAME_array[$i]}"
  var=$((i+1))
  echo $var
  if sudo ovs-vsctl --data=bare --no-heading --columns=name find interface external_ids:container_id=docker-build-ev-int_ssh_server-$var \
      external_ids:container_iface=eth1 | grep -q "${!PORT_NAME_array[$i]}_l"; then
      sudo ./my-ovs-docker del-port br0 eth1 docker-build-ev-int_ssh_server-$var
  fi
  sudo docker stop docker-build-ev-int_ssh_server-$var
  sudo docker start docker-build-ev-int_ssh_server-$var
  sudo ./my-ovs-docker add-port br0 eth1 docker-build-ev-int_ssh_server-$var ${PORT_NAME_array[$i]} ${PORT_array[$i]} \
    --ipaddress=${IP_array[$i]} --macaddress=${MAC_array[$i]}
  sudo ovs-vsctl -- set port ${PORT_NAME_array[$i]}_l tag=1
  sudo iptables -t nat -A POSTROUTING -o ${PORT_NAME_array[$i]}_l -j MASQUERADE
done
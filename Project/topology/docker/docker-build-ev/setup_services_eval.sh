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
192.168.3.22/24
192.168.3.23/24
192.168.3.24/24
192.168.3.25/24
192.168.3.26/24
192.168.3.27/24
192.168.3.28/24
192.168.3.29/24
192.168.3.30/24
192.168.3.31/24
192.168.3.32/24
192.168.3.33/24
192.168.3.34/24
192.168.3.35/24
192.168.3.36/24
192.168.3.37/24
192.168.3.38/24
192.168.3.39/24
192.168.3.40/24
192.168.3.41/24
192.168.3.42/24)
# 192.168.3.43/24
# 192.168.3.44/24
# 192.168.3.45/24
# 192.168.3.46/24
# 192.168.3.47/24
# 192.168.3.48/24
# 192.168.3.49/24
# 192.168.3.50/24
# 192.168.3.51/24
# 192.168.3.52/24)

MAC_array=(08:00:27:b6:d0:69
08:00:27:b6:d0:70
08:00:27:b6:d0:71
08:00:27:b6:d0:72
08:00:27:b6:d0:73
08:00:27:b6:d0:74
08:00:27:b6:d0:75
08:00:27:b6:d0:76
08:00:27:b6:d0:77
08:00:27:b6:d0:78
08:00:27:b6:d0:79
08:00:27:b6:d0:80
08:00:27:b6:d0:81
08:00:27:b6:d0:82
08:00:27:b6:d0:83
08:00:27:b6:d0:84
08:00:27:b6:d0:85
08:00:27:b6:d0:86
08:00:27:b6:d0:87
08:00:27:b6:d0:88
08:00:27:b6:d0:89
08:00:27:b6:d0:90
08:00:27:b6:d0:91
08:00:27:b6:d0:92
08:00:27:b6:d0:93
08:00:27:b6:d0:94
08:00:27:b6:d0:95
08:00:27:b6:d0:96
08:00:27:b6:d0:97
08:00:27:b6:d0:98)
# 08:00:27:b6:d1:89
# 08:00:27:b6:d1:90
# 08:00:27:b6:d1:91
# 08:00:27:b6:d1:92
# 08:00:27:b6:d1:93
# 08:00:27:b6:d1:94
# 08:00:27:b6:d1:95
# 08:00:27:b6:d1:96
# 08:00:27:b6:d1:97
# 08:00:27:b6:d1:98)


PORT_array=(26
27
28
29
30
31
32
33
34
35
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65)
# 66
# 67
# 68
# 69
# 70
# 71
# 72
# 73
# 74
# 75)


PORT_NAME_array=("h3"
"h4"
"h5"
"h6"
"h7"
"h8"
"h9"
"h10"
"h11"
"h12"
"h13"
"h14"
"h15"
"h16"
"h17"
"h18"
"h19"
"h20"
"h21"
"h22"
"h23"
"h24"
"h25"
"h26"
"h27"
"h28"
"h29"
"h30"
"h31"
"h32")
# "h33"
# "h34"
# "h35"
# "h36"
# "h37"
# "h38"
# "h39"
# "h40"
# "h41"
# "h42")


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
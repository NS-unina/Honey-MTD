from network import Host, Honeypot, Attacker, Subnet, Network, Gateway

#------- NETWORK TOPOLPOGY -------------------------------------------------------------- #    
# Nodes
host = Host('host', '192.168.3.10', '08:00:27:b6:d0:66', 15, '255.255.255.0')
service = Host('service', '192.168.3.11', '08:00:27:6d:ec:62', 3, '255.255.255.0')
ssh_service = Host('ssh_service', '192.168.3.13', '08:00:27:b6:d0:69', 16, '255.255.255.0')
heralding = Honeypot('heralding', '192.168.3.12', '08:00:27:6c:0a:bf', 4, '255.255.255.0')

s1 = Host('s1', '192.168.3.14', '08:00:27:b6:d0:70', 27, '255.255.255.0')
s2 = Host('s2', '192.168.3.15', '08:00:27:b6:d0:71', 28, '255.255.255.0')
s3 = Host('s3', '192.168.3.16', '08:00:27:b6:d0:72', 29, '255.255.255.0')
s4 = Host('s4', '192.168.3.17', '08:00:27:b6:d0:73', 30, '255.255.255.0')
s5 = Host('s5', '192.168.3.18', '08:00:27:b6:d0:74', 31, '255.255.255.0')
s6 = Host('s6', '192.168.3.19', '08:00:27:b6:d0:75', 32, '255.255.255.0')
s7 = Host('s7', '192.168.3.20', '08:00:27:b6:d0:76', 33, '255.255.255.0')
s8 = Host('s8', '192.168.3.21', '08:00:27:b6:d0:77', 34, '255.255.255.0')
s9 = Host('s9', '192.168.3.22', '08:00:27:b6:d0:78', 35, '255.255.255.0')
s10 = Host('s10', '192.168.3.23', '08:00:27:b6:d0:79', 36, '255.255.255.0')

cowrie = Honeypot('cowrie', '192.168.4.10', '08:00:27:b7:0e:58', 6, '255.255.255.0')
heralding1 = Honeypot('heralding1', '192.168.4.11', '08:00:27:6d:f9:98', 13, '255.255.255.0')

elk_if1 = Host('ELK_IF1', '192.168.5.10', '08:00:27:7d:b7:b8', 8, '255.255.255.0')
elk_if2 = Host('ELK_IF2', '192.168.11.10', '08:00:27:f5:6b:90', 13, '255.255.255.0')

dmz_heralding = Honeypot('dmz_heralding', '192.168.10.10', '08:00:27:2c:30:92', 2, '255.255.255.0')
dmz_service = Host('dmz_service', '192.168.10.11', '08:00:27:b6:d0:67', 22, '255.255.255.0')
dmz_service1 = Host('dmz_service1', '192.168.10.14', '08:00:27:6d:ec:74', 21, '255.255.255.0')
dmz_cowrie = Honeypot('dmz_cowrie', '192.168.10.13', '08:00:27:b7:0e:59', 20, '255.255.255.0')
dmz_host = Host('dmz_host', '192.168.10.12', '08:00:27:b6:d0:68', 23, '255.255.255.0')

# Subnets
# ovs1
subnet1 = Subnet('S1', '192.168.3.0', '255.255.255.0')
subnet2 = Subnet('S2', '192.168.4.0', '255.255.255.0')
subnet3 = Subnet('S3', '192.168.5.0', '255.255.255.0')
#ovs2
subnet4 = Subnet('S4', '192.168.10.0', '255.255.255.0')
subnet5 = Subnet('S5', '192.168.11.0', '255.255.255.0')

# Gateways
# ovs1
gw1 = Gateway('gw1', '192.168.3.1', '9e:c3:c6:49:0e:e8', 1, '255.255.255.0')
gw2 = Gateway('gw2', '192.168.4.1', '16:67:1f:3f:86:a7', 5, '255.255.255.0')
gw3 = Gateway('gw3', '192.168.5.1', 'fe:46:67:35:0d:d1', 7, '255.255.255.0')
# ovs2
gw10 = Gateway('gw10', '192.168.10.1', '8a:ae:02:40:8f:93', 40, '255.255.255.0')
gw11 = Gateway('gw11', '192.168.11.1', 'ea:6a:20:a0:96:11', 41, '255.255.255.0')

# Network
network1 = Network('Net1')
network2 = Network('Net2')

# Add nodes to subnets
# ovs1
subnet1.add_node(host, host.get_ovs_port())
subnet1.add_node(heralding, heralding.get_ovs_port())
subnet1.add_node(service, service.get_ovs_port())
subnet1.add_node(ssh_service, ssh_service.get_ovs_port())
subnet1.add_node(gw1, gw1.get_ovs_port())

subnet2.add_node(cowrie, cowrie.get_ovs_port())
subnet2.add_node(heralding1, heralding1.get_ovs_port())
subnet2.add_node(gw2, gw2.get_ovs_port())

subnet3.add_node(elk_if1, elk_if1.get_ovs_port())
subnet3.add_node(gw3, gw3.get_ovs_port())

#ovs2
subnet4.add_node(dmz_service, dmz_service.get_ovs_port())
subnet4.add_node(dmz_heralding, dmz_heralding.get_ovs_port())
subnet4.add_node(dmz_host, dmz_host.get_ovs_port())
subnet4.add_node(dmz_cowrie, dmz_cowrie.get_ovs_port())
subnet4.add_node(dmz_service1, dmz_service1.get_ovs_port())
subnet4.add_node(gw10, gw10.get_ovs_port())

subnet5.add_node(elk_if2, elk_if2.get_ovs_port())
subnet5.add_node(gw11, gw11.get_ovs_port())


# Add subnets to network
network1.add_subnet(subnet1)
network1.add_subnet(subnet2)
network1.add_subnet(subnet3)

network2.add_subnet(subnet4)
network2.add_subnet(subnet5)

ports = [5432, 143, 5900, 3306]

br0_dpid = 64105189026373
br1_dpid = 64105189026374

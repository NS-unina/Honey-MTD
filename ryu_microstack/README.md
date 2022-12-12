# SkyTrap-MTD

## Microstack    
Setting up the infrastructure with Microstack using one OpenvSwitch and VxLAN protocol.

At first in OpenStack environment create a Network with a Subnet. Connect it to the external Network through a router. 

Create 7 instances (Image: Ubuntu 20.04, Flavor: Custom) and connect them to this Network:
1. OpenvSwitch
2. Ryu Controller
3. Attacker Host
4. Honeypot Host
5. h11 Host
6. h12 Host
7. h13 Host

Associate them a Floating-IP in order to reach them from the outside through ssh.

1. In the Host "OpenvSwitch" shell, first install openvswitch: 
``` 
sudo apt update
sudo apt upgrade
sudo apt-get install openvswitch-switch
``` 

2. In OpenvSwitch shell also put those commands to create the switch:
```  
ovs-vsctl add-br br0
ovs-vsctl add-port br0 br0-int -- set interface br0-int type=internal 
```    

3. In each Host (controller and switch excluded) shell put those commands to connect the host to the switch using VxLAN:  
```  
ovs-vsctl add-br br0
ovs-vsctl add-port br0 br0-int -- set interface br0-int type=internal
sudo ovs-vsctl add-port br0 vx1 -- set interface vx1 type=vxlan options:remote_ip=10.0.1.118 <switch ip> options:key=2001
```   

4. Now in OpenvSwitch shell insert this command to connect it to the host:
```  
sudo ovs-vsctl add-port br0 vx2<port-name> -- set interface vx2<interface-name> type=vxlan options:remote_ip=10.0.1.24 <host ip> options:key=2001
``` 
5. Then in OpenvSwitch shell insert this command to associate it to a controller:
```  
ovs-vsctl set bridge br0 protocols=OpenFlow13 -- set-controller br0 tcp:10.0.1.150 <controller ip>:6633 
```   
6. On each host (controller and switch excluded) insert this command in order to assing them an IP address for the overlay network:
```  
sudo ifconfig br0-int 200.0.0.102 <new ip host> mtu 1400 up
``` 
7. Finally on the Controller machine install ryu and run one of the default Ryu Controllers:
```  
pip install ryu
pip install eventlet==0.30.2
ryu-manager ryu.app.simple_switch_13
``` 

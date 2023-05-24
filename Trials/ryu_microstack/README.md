# MicroStack-OpenStack Configuration

## Prerequirements

1. Access to OpenStack Dashboard.
2. Create a new Project associated to your preferred account.

**Compute Resources**:
1. An Image with Ubuntu 20.04 (Minimum Disk 8 GB, Minimum RAM 512 MB).
2. A First Flavor with at least 20 GB of Root Disk, 4 GB of RAM and 2 CPU.
3. A Second Flavor with at least 10 GB of Root Disk and 1 GB of RAM  and 1 CPU.
4. One or more *private keys* that you 'll associate to your instances.

**Network Resources**:
1. An external network (default).
2. Another *network1*, with a subnet *subnet1*.
3. A *router* that 'll allow allow the network1 instances to be reachable from the outside. It has two interfaces, the first toward the external network and the second toward network1.
4. Another *security group* in which you allow all SSH connections (TCP, port 22), and permit ICMP packets.
5. Seven (one for instance) Floating IPs, in order to reach the internal host from the outside (NAT).

**Instances**:

Now, in the Compute section, we create 7 Instances connected to the internal network *network1*:
- **OpenvSwitch** --> **Image**: *Ubuntu 20.04*; **Flavor**: *First_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **Controller**  --> **Image**: *Ubuntu 20.04*; **Flavor**: *First_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **Attacker**    --> **Image**: *Ubuntu 20.04*; **Flavor**: *Second_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **Honeypot**    --> **Image**: *Ubuntu 20.04*; **Flavor**: *Second_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **h11**         --> **Image**: *Ubuntu 20.04*; **Flavor**: *Second_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **h12**         --> **Image**: *Ubuntu 20.04*; **Flavor**: *Second_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.
- **h13**         --> **Image**: *Ubuntu 20.04*; **Flavor**: *Second_Flavor*; **KeyPair**: *key_pair*; **IP Address**: *Internal IP* + *Floating IP*.

Remember to associate the new security group to each Instance.

## Overlay Network Configuration

We 'll configure an overlay network on top of the previous created with Openstack. For this purpose we 'll use *Open vSwitch* combined with the *VxLAN protocol* in order to create links between Open vSwitch and the hosts.

To access though *ssh* into one of the instances:

```
$ ssh -i key_pair.pem ubuntu@Floating_IP_of_the_instance
```
**NB**: Remember to enable ipv4_forwarding on your machine.

In each instance,  except Controller, install *Open vSwitch* in this way:

```
$ sudo apt update

$ sudo apt upgrade

$ sudo apt install openvswitch-switch
```
### OpenvSwitch Configuration

Enter in the OpenvSwitch shell, that now is only a simple Ubuntu host. We need to create a virtual switch.

```
$ sudo ovs-vsctl add-br br0 

$ sudo ovs-vsctl add-port br0 br0-int --set interface br0-int type=internal
```
In this way we have created a bridge/switch with an internal interface *br0-int*.

Now we have to connect the switch to each host in the subnet using VxLAN interfaces. Type this command for each host you want to connect to switch.

```
$ sudo ovs-vsctl add-port br0 <interface-name> --set interface <interface-name> type=vxlan options:remote_ip=<host-IP> options:key=2001
```
Finally set the Controller.

```
$ sudo ovs-vsctl set bridge br0 protocols=OpenFlow13 -- set-controller br0 tcp:<controller-IP>:6633
```
Some commands that will be useful during the configuration:

1. To show ovs ports associated to each interface:

```
$ sudo ovs-vsctl -- --columns=name,ofport list Interface
```
2. To show the content of Switch Flow Table:

```
$ sudo ovs-ofctl -O OpenFlow13 dump-flows br0 
```
### Controller Configuration

We will use a *Ryu* Controller. You need to install Ryu on Controller host.

```
$ pip install ryu

$ pip install eventlet==0.30.2
```
### Hosts Configuration

These steps will need to be repeated for each host to connect to the switch.

```
$ sudo ovs-vsctl add-br br0

$ sudo ovs-vsctl add-port br0 br0-int -- set interface br0-int type=internal

$ sudo ovs-vsctl add-port <interface-name> -- set interface <interface-name> type=vxlan options:remote_ip=<switch-IP> options:key=2001 
```
Finally assign IP and MAC addresses to the internal interface, and setting up it using the *ifconfig* tool.

```
$ sudo ifconfig br0-int <host_overlay_IP> mtu 1400 up 

$ sudo ifconfig br0-int hw ether <host_overlay_MAC> 
```

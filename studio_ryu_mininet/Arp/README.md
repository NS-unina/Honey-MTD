# SkyTrap-MTD

## Examples description
The folder *Arp* includes two subfolders:

1. In **topo_with_honeypot** the topology file includes the honeypot as a simple host. The *attacker* is supposed to be the host h10 (IP: 10.0.1.10/24). The *honeypot* is the host h200 (IP: 10.0.1.200/24). In the attacker's subnet there are also two other hosts (h11 IP: 10.0.1.11/24; h12 IP: 10.0.1.12/24).


1. Run the controller:
``` 

ryu-manager controller1_0.py
``` 

2. Run mininet environment:
```
sudo python topology1_0.py
```

Now you can test the environment.

1. **Arp-Scan**
From the *attacker* shell:

``` 
h10 arp-scan -l
``` 

or
``` 
h10 nmap -sn 10.0.1.0/24
``` 
You 'll se only what the controller wants to show you: the honeypot and the host h12.


2. **Ping redirection**


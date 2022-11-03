
# SkyTrap-MTD

## Examples description
The folder *Arp* includes two subfolders:

- In **topo_with_honeypot** the topology file includes the honeypot as a simple host. The *attacker* is supposed to be the host h10 (IP: 10.0.1.10/24). The *honeypot* is the host h200 (IP: 10.0.1.200/24). In the attacker's subnet there are also two other hosts (h11 IP: 10.0.1.11/24; h12 IP: 10.0.1.12/24).


1. Run the controller:
``` 
ryu-manager controller1_0.py
``` 

2. Run mininet environment:
```
sudo python topology1_0.py
```

Now you can test the environment.

**Arp-Scan**
From the *attacker* shell:

``` 
h10 arp-scan -l
``` 

or
``` 
h10 nmap -sn 10.0.1.0/24
``` 
You 'll se only what the controller wants to show you: the honeypot and the host h12.


**Ping redirection**
From the *attacker* shell:
```
h10 ping h12
``` 
You 'll receive the response from honeypot unstead host h12.

+ In **topo_without_honeypot** the topology doesn't include the honeypot as an host. The controller simulates it making it visible only to the attacker, but it is not a real host. 
The execution is the same of previous example.
It supports only *arp-scan* because the honeypot is unreachable. 






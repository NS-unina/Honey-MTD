


# SkyTrap-MTD

## DA RISCRIVERE
The folder *Project* includes two subfolders:

- In **topo_with_honeypot** the topology file includes the honeypot as a simple host. The *attacker* is supposed to be the host h10 (IP: 10.0.1.10/24). The *honeypot* is the host h200 (IP: 10.0.1.200/24). In the attacker's subnet there are also three other hosts (h11 IP: 10.0.1.11/24; h12 IP: 10.0.1.12/24; h13 IP: 10.0.1.13/24).


1. Run the controller:
``` 
ryu-manager controller1_0.py
``` 

2. Run mininet environment:
```
sudo python topology1_0.py
```

If you want to re-start the enviroment, before to do it, remember to fresh the topology on your system:
```
sudo mn -c
```

**Arp-Scan**

- Tabella con regole inserite


```
h10 arp-scan -l
```

**Ping Scan**

- Tabella con regole inserite per ICMP

```
h10 nmap -PE 10.0.1.0/24 --disable-arp-ping
```

**TCP Scan**

- Tabella con regole inserite per TCP
- Esecuzione http server su honeypot e host h13 per simulazione redirection

```
h10 nmap -PS 10.0.1.0/24 --disable-arp-ping
```
**UDP Scan**

- Tabella con regole inserite per UDP
- Esecuzione server udp su honeypot e host h13 per simulazione redirection

```
h10 nmap -PU 10.0.1.0/24 --disable-arp-ping --max-retries 0 --min-rate 5000
```

- Flag inseriti per velocizzare UDP scan

+ In **topo_without_honeypot** the topology doesn't include the honeypot as an host. The controller simulates it making it visible only to the attacker, but it is not a real host. 
The execution is the same of previous example.
It supports only *arp-scan* because the honeypot is unreachable. 









# SkyTrap-MTD

## Policies
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

- *IP attacker* : 10.0.1.10/24
- *IP honeypot* : 10.0.1.200/24

Rules inserted:
```
| Sender IP     | Target IP      | Type 	   | Action |
| ------------- | -------------  | ------------       | ------ |
| 10.0.1.10/24  | 10.0.1.11/24   | ARP REQUEST        | DROP   |
| 10.0.1.10/24  | 10.0.1.200/24  | ARP REQUEST        | PERMIT |
| 10.0.1.10/24  | 10.0.1.12/24   | ARP REQUEST        | PERMIT |
| 10.0.1.10/24  | 10.0.1.13/24   | ARP REQUEST        | PERMIT |
| 10.0.1.11/24  | 10.0.1.10/24   | ARP REPLY          | DROP   |
| 10.0.1.11/24  | 10.0.1.200/24  | ARP REQUEST        | DROP   |
| 10.0.1.12/24  | 10.0.1.200/24  | ARP REQUEST        | DROP   |
| 10.0.1.13/24  | 10.0.1.200/24  | ARP REQUEST        | DROP   |
| 10.0.1.11/24  | 10.0.1.12/24   | ARP REQUEST/REPLY  | PERMIT |
| 10.0.1.11/24  | 10.0.1.13/24   | ARP REQUEST/REPLY  | PERMIT |
| 10.0.1.12/24  | 10.0.1.11/24   | ARP REQUEST/REPLY  | PERMIT |
| 10.0.1.12/24  | 10.0.1.13/24   | ARP REQUEST/REPLY  | PERMIT |
| 10.0.1.13/24  | 10.0.1.11/24   | ARP REQUEST/REPLY  | PERMIT |
| 10.0.1.13/24  | 10.0.1.12/24   | ARP REQUEST/REPLY  | PERMIT |


```


To make an ARP scan in the subnet 10.0.1.0/24, insert this command in the attacker shell:
```
h10 arp-scan -l
```

**Ping Scan**

- *IP attacker* : 10.0.1.10/24
- *IP honeypot* : 10.0.1.200/24


Rules:

```

| Sender IP     | Receiver IP      | Type 	      | Action      |
| ------------- | -------------  | ------------       | ------     |
| 10.0.1.10/24  | 10.0.1.11/24   | ECHO REQUEST       | DROP       |
| 10.0.1.10/24  | 10.0.1.12/24   | ECHO REQUEST       | DROP       |
| 10.0.1.10/24  | 10.0.1.13/24   | ECHO REQUEST       | REDIRECT   |
| 10.0.1.10/24  | 10.0.1.200/24  | ECHO REQUEST       | PERMIT     |
| 10.0.1.11/24  | 10.0.1.10/24   | ECHO REQUEST       | DROP       |
| 10.0.1.12/24  | 10.0.1.10/24   | ECHO REQUEST       | DROP       |
| 10.0.1.13/24  | 10.0.1.10/24   | ECHO REQUEST       | DROP       |
| 10.0.1.200/24 | 10.0.1.10/24   | ECHO REPLY         | CHANGE SRC |
| 10.0.1.11/24  | 10.0.1.12/24   | ECHO REQUEST/REPLY | PERMIT     |
| 10.0.1.11/24  | 10.0.1.13/24   | ECHO REQUEST/REPLY | PERMIT     |
| 10.0.1.12/24  | 10.0.1.11/24   | ECHO REQUEST/REPLY | PERMIT     |
| 10.0.1.12/24  | 10.0.1.13/24   | ECHO REQUEST/REPLY | PERMIT     |
| 10.0.1.13/24  | 10.0.1.11/24   | ECHO REQUEST/REPLY | PERMIT     |
| 10.0.1.13/24  | 10.0.1.12/24   | ECHO REQUEST/REPLY | PERMIT     |


```

To make a PING scan in the subnet 10.0.1.0/24, insert this command in the attacker shell:
```
h10 nmap -PE 10.0.1.0/24 --disable-arp-ping
```

**TCP Scan**

- *IP attacker* : 10.0.1.10/24
- *IP honeypot* : 10.0.1.200/24


Rules:

```
| Sender IP     | Receiver IP    | Type 		| Action     |
| ------------- | -------------  | ------------       | ------     |
| 10.0.1.10/24  | 10.0.1.12/24   |  ANY               | DROP       |
| 10.0.1.10/24  | 10.0.1.200/24  |  ANY               | PERMIT     |
| 10.0.1.10/24  | 10.0.1.13/24   |  ANY               | REDIRECT   |
| 10.0.1.200/24 | 10.0.1.10/24   |  ANY               | CHANGE SRC |
| 10.0.1.11/24  | 10.0.1.12/24   |  ANY               | PERMIT     |
| 10.0.1.11/24  | 10.0.1.13/24   |  ANY               | PERMIT     |
| 10.0.1.12/24  | 10.0.1.11/24   |  ANY               | PERMIT     |
| 10.0.1.12/24  | 10.0.1.13/24   |  ANY               | PERMIT     |
| 10.0.1.13/24  | 10.0.1.11/24   |  ANY               | PERMIT     |
| 10.0.1.13/24  | 10.0.1.12/24   |  ANY               | PERMIT     |
| 

```

- Before, you can run the python SimpleHTTPServer on host h13 and on honeypot shell writing the following command line:

```
h13 python -m http.server 80 &

h200 python -m http.server 8080 &
```


To make a TCP SYN/ACK scan in the subnet 10.0.1.0/24, insert this command in the attacker shell:
```
h10 nmap -PS/-PA 10.0.1.0/24 --disable-arp-ping
```
**UDP Scan**

- *IP attacker* : 10.0.1.10/24
- *IP honeypot* : 10.0.1.200/24

Rules: 

```
| Sender IP     | Receiver IP    | Type 		      | Action     |
| ------------- | -------------  | ------------       | ------     |
| 10.0.1.10/24  | 10.0.1.12/24   |  ANY               | DROP       |
| 10.0.1.10/24  | 10.0.1.200/24  |  ANY               | PERMIT     |
| 10.0.1.10/24  | 10.0.1.13/24   |  ANY               | REDIRECT   |
| 10.0.1.200/24 | 10.0.1.10/24   |  ANY               | CHANGE SRC |
| 10.0.1.11/24  | 10.0.1.12/24   |  ANY               | PERMIT     |
| 10.0.1.11/24  | 10.0.1.13/24   |  ANY               | PERMIT     |
| 10.0.1.12/24  | 10.0.1.11/24   |  ANY               | PERMIT     |
| 10.0.1.12/24  | 10.0.1.13/24   |  ANY               | PERMIT     |
| 10.0.1.13/24  | 10.0.1.11/24   |  ANY               | PERMIT     |
| 10.0.1.13/24  | 10.0.1.12/24   |  ANY               | PERMIT     |
| 

```

- Esecuzione server udp su honeypot e host h13 per simulazione redirection

To make a TCP SYN/ACK scan in the subnet 10.0.1.0/24, insert this command in the attacker shell:
```
h10 nmap -PU 10.0.1.0/24 --disable-arp-ping --max-retries 0 --min-rate 5000
```

- Flag inseriti per velocizzare UDP scan

+ In **topo_without_honeypot** the topology doesn't include the honeypot as an host. The controller simulates it making it visible only to the attacker, but it is not a real host. 
The execution is the same of previous example.
It supports only *arp-scan* because the honeypot is unreachable. 






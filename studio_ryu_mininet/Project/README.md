


# SkyTrap-MTD

## DA RISCRIVERE
The folder *Project* includes two subfolders:

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

Host h12 is the decoy used to simulate *ping redirection*.

From the *attacker* shell:
```
h10 ping h12
``` 
You 'll receive the response from honeypot unstead host h12.

**HTTP request redirection (TCP test)**

Host h13 is the decoy used to simulate *HTTP Request redirection*. 

Restart the environment. 

Remember to fresh the topology on your system:
```
sudo mn -c
```

First of all from host 13 run the python *SimpleHTTPServer* listening on port 80 in background:
```
h13 python -m http.server 80 &
```
Then do the same from honeypot, but listening on port 8080:
```
h200 python -m http.server 8080 &
```

After that, from the attacker send an HTTP request to the host h13, using the *wget* tool:
```
h10 wget h13
```
Your request will be redirected to the honeypot through the controller.
It also manage properly its response.

**NTP request redirection (UDP test)**

Restart the environment.

After that, run the *UDP server* listening in background on port 123, in the host h13 shell:
```
h13 sudo python ./udp_server/server.py --port 123 &
```
Than, run another *UDP server*listening in background on port 53, in the honeypot shell:
```
h200 sudo python ./udp_server/server.py --port 53 &
```
Now, execute the script *client.py* from the attacker shell. It 'll make a simple NTP request through the UDP transport protocol against the decoy host h13:
```
h10 ./udp_server/client.py --host h13 --port 123
```
The request will be intercepted by the controller, which redirects it to the honeypot. 

+ In **topo_without_honeypot** the topology doesn't include the honeypot as an host. The controller simulates it making it visible only to the attacker, but it is not a real host. 
The execution is the same of previous example.
It supports only *arp-scan* because the honeypot is unreachable. 






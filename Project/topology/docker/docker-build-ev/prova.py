from random import randint
import subprocess

IP=["192.168.3.10",
"192.168.3.11",
"192.168.3.12",
"192.168.3.13",
"192.168.3.14",
"192.168.3.15",
"192.168.3.16",
"192.168.3.17",
"192.168.3.18",
"192.168.3.19",
"192.168.3.20",
"192.168.3.21",
"192.168.3.22"]

t = []
i = 0
while len(t) < len(IP):
    x = randint(0, len(IP) - 1)
    z = t.count(IP[x])
    if z > 0:
        pass
    else:
        t.append(IP[x])
        arg = IP[x]
        n = str(i)
        subprocess.check_call(['./check.sh', arg, n])
        i = i + 1

from random import randint
import subprocess

IP=["192.168.3.10",
"192.168.3.11",
"192.168.3.12",
"192.168.3.13"]

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

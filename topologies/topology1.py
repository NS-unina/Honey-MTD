from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology1():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    #Routers
    #r1 = net.addHost('r1')
    r1 = net.addSwitch('r1')

    #Hosts
    attacker = net.addHost('attacker', ip = '192.168.10.2', mac = '18:AD:27:7C:33:5E')
    h1 = net.addHost('h1', ip = '192.168.30.2', mac = '19:AD:27:7C:33:5E')
    h2 = net.addHost('h2', ip = '192.168.20.2', mac = '3F:F5:B8:AD:55:04')
    h3 = net.addHost('h3', ip = '192.168.40.2', mac = '4F:F5:B8:AD:55:04')

    #Controller
    c0 = net.addController('c0', controller=RemoteController, ip = '127.0.0.1', port = 6633)

    #Set Links
    net.addLink(attacker, r1)
    net.addLink(r1, h1)
    net.addLink(r1, h2)
    net.addLink(r1, h3)

    #Build network
    net.build()

    #Start controller
    c0.start()

    r1.start([c0])  #Questo metodo start associa il controller allo switch (lo hanno solo gli switch?)
    
    #Configurazione interfacce router
    r1.cmd('ifconfig r1-eth0 0')
    r1.cmd('ifconfig r1-eth1 0')
    r1.cmd('ifconfig r1-eth2 0')
    r1.cmd('ifconfig r1-eth3 0')


    #Configurazione MAC address interfacce di rete router
    r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")
    r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:02")
    r1.cmd("ifconfig r1-eth2 hw ether 00:00:00:00:01:03")
    r1.cmd("ifconfig r1-eth3 hw ether 00:00:00:00:01:04")

    #Configurazione IP address interfacce router
    r1.cmd("ip addr add 192.168.10.1 brd + dev r1-eth0")
    r1.cmd("ip addr add 192.168.30.1 brd + dev r1-eth1")
    r1.cmd("ip addr add 192.168.20.1 brd + dev r1-eth2")
    r1.cmd("ip addr add 192.168.40.1 brd + dev r1-eth3")

    #Abilito IP forwarding
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #Default gateway
    attacker.cmd("ip route add default via 192.168.10.1")
    h1.cmd("ip route add default via 192.168.30.1")
    h2.cmd("ip route add default via 192.168.20.1")
    h3.cmd("ip route add default via 192.168.40.1")


    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology1()
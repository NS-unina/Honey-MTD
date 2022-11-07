from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController


class Topology1(Topo):
    """Topology 1"""
    def build(self):

        # Attacker in subnet 10.0.1.0/24
        h10 = self.addHost('h10', mac='00:00:00:00:00:01', ip='10.0.1.10/24', defaultRoute="h10-eth0")

        # Simple Hosts in subnet 10.0.1.0/24
        h11 = self.addHost('h11', mac='00:00:00:00:00:02', ip='10.0.1.11/24', defaultRoute="h11-eth0")
        h12 = self.addHost('h12', mac='00:00:00:00:00:03', ip='10.0.1.12/24', defaultRoute="h12-eth0")
        h13 = self.addHost('h13', mac='00:00:00:00:00:05', ip='10.0.1.13/24', defaultRoute="h13-eth0")

        # Honeypot in subnet 10.0.1.0/24
        h200 = self.addHost('h200', mac='00:00:00:00:00:09', ip='10.0.1.200/24', defaultRoute="h200-eth0")

        # Simple Host in subnet 10.0.2.0/24
        h20 = self.addHost('h20', mac='00:00:00:00:00:04', ip='10.0.2.20/24', defaultRoute="h20-eth0")


        # Routers
        s_1 = self.addSwitch('s_1')
        s_2 = self.addSwitch('s_2')


        self.addLink(s_1, h10, port1=1, port2=0)
        self.addLink(s_1, h11, port1=2, port2=0)
        self.addLink(s_1, h12, port1=3, port2=0)
        self.addLink(s_1, h13, port1=8, port2=0)
        self.addLink(s_1, h200, port1=7, port2=0)

        self.addLink(s_2, h20, port1=4, port2=0)

        self.addLink(s_1, s_2, port1=5, port2=6)

def configure():
    """Docstring"""
    topo = Topology1()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()
    CLI(net) 
    net.stop()

if __name__ == '__main__':
    configure()

#Jacob McClure
#jatmcclu@ucsc.edu

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    h10 = self.addHost('h10',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h10-eth0")
    h20 = self.addHost('h20',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h20-eth0")
    h30 = self.addHost('h30',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h30-eth0")
    # trusted host
    h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='104.82.214.112/24', defaultRoute="h4-eth0")
    # untrusted host
    h5 = self.addHost('h5',mac='00:00:00:00:00:05',ip='156.134.2.12/24', defaultRoute="h5-eth0")
    # server   
    h6 = self.addHost('h6',mac='00:00:00:00:00:06',ip='10.0.4.10/24', defaultRoute="h6-eth0")

    # Create switches for: each floor (1,2,3) and the Core/Data Center 
    s1 = self.addSwitch('s1') # floor 1
    s2 = self.addSwitch('s2') # floor 2
    s3 = self.addSwitch('s3') # floor 3
    s4 = self.addSwitch('s4') # Core switch
    s5 = self.addSwitch('s5') # Data Center switch

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host being connected
    # Link switches for floors 1,2,3 to hosts 10,20,30 respectively
    self.addLink(s1, h10, port1=1, port2=0)
    self.addLink(s2, h20, port1=2, port2=0)
    self.addLink(s3, h30, port1=3, port2=0)
    
    # Link Core switch to Trusted Host & Untrusted Host
    self.addLink(s4, h4, port1=4, port2=0)
    self.addLink(s4, h5, port1=5, port2=0)
    
    # Link Data Center switch to Server
    self.addLink(s5, h6, port1=6, port2=0)
    
    # Link Core switch to: floor (1,2,3) switch and Data Center 
    self.addLink(s4, s1, port1=7, port2=11)
    self.addLink(s4, s2, port1=8, port2=12)
    self.addLink(s4, s3, port1=9, port2=13)
    self.addLink(s4, s5, port1=10, port2=14)

# pulls config / initializes the topology
def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  CLI(net) 
  net.stop()

if __name__ == '__main__':
  configure()

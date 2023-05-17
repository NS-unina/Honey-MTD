class Node:
    def __init__(self, name = None, ip_addr = None, MAC = None, ovs_port = 0, netmask = None):
        self.name = name
        self.ip_addr = ip_addr
        self.MAC = MAC
        self.ovs_port = ovs_port
        self.netmask = netmask

    # GET METHODS
    def get_name(self):
        return self.name
    
    def get_ip_addr(self):
        return self.ip_addr

    def get_MAC_addr(self): 
        return self.MAC

    def get_ovs_port(self):
        return self.ovs_port
    
    def get_netmask(self):
        return self.netmask

    # SET METHODS
    def set_name(self, name):
        self.name = name
    
    def set_ip_addr(self, ip):
        self.ip_addr = ip
    
    def set_MAC_addr(self, mac):
        self.MAC = mac
    
    def set_ovs_port(self, gp):
        self.ovs_port = gp
    
    def set_netmask(self, netmask):
        self.netmask = netmask

class Host(Node):
    def __init__(self, name=None, ip_addr=None, MAC=None, ovs_port=0, netmask=None):
        super().__init__(name, ip_addr, MAC, ovs_port, netmask)
        # Poi eventualmente aggiungi attributi e/o funzioni

class Honeypot(Node):
    def __init__(self, name=None, ip_addr=None, MAC=None, ovs_port=0, netmask=None, type = None):
        super().__init__(name, ip_addr, MAC, ovs_port, netmask)
        self.type = type

class Gateway(Node):
    def __init__(self, name=None, ip_addr=None, MAC=None, ovs_port=0, netmask=None):
        super().__init__(name, ip_addr, MAC, ovs_port, netmask)

class Service(Node):
    def __init__(self, name=None, ip_addr=None, MAC=None, ovs_port=0, netmask=None, port=None):
        super().__init__(name, ip_addr, MAC, ovs_port, netmask)
        self.port = port

    def get_port(self):
        return self.port

    def set_port(self, p):
        self.port = p
        
class Attacker(Node):
    def __init__(self, name=None, ip_addr=None, MAC=None, ovs_port=0, netmask=None, network=None):
        super().__init__(name, ip_addr, MAC, ovs_port, netmask)
        self.network = network

class Subnet:
    def __init__(self, subnet_name = None, ip_addr = None, netmask = None):
        self.subnet_name = subnet_name
        self.ip_addr = ip_addr
        self.netmask = netmask
        self.nodes = dict()     # host, honeypot, server, gateway 

        # la chiave di ogni elemento è la porta del gateway a cui i vari nodi sono collegati

    # Port = 0 if the node is the gateway
    def add_node(self, node, port):
        self.nodes[port] = node


class Network:
    def __init__(self, name):
        self.name = name
        self.subnets = list()

    def add_subnet(self, subnet):
        self.subnets.append(subnet)


    
        
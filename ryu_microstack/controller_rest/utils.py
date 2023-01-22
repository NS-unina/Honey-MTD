from network import Subnet
import random

class Utils():

    @staticmethod
    def host_to_port(subnet : Subnet, host_ip):
        out_port = None
        nodes = subnet.nodes
        for k, v in nodes.items():
            ip = v.get_ip_addr()
            if ip == host_ip:
               out_port = k
        return out_port
    
    @staticmethod
    def host_to_mac(subnet : Subnet, host_ip):
        mac = None
        nodes = subnet.nodes
        for k, v in nodes.items():
            ip = v.get_ip_addr()
            if ip == host_ip:
                mac = v.get_MAC_addr()
        return mac
    
    @staticmethod
    def make_new_IP(ips, sub):
        while(True):
            if len(ips) == 251:
                ips.clear()
            new_ip = sub + str(random.randint(2, 253))
            if new_ip not in ips:
                ips.append(new_ip)
                break
        return new_ip
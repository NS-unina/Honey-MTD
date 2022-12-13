from network import Subnet

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
              
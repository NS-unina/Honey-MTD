import json

from controller import ExampleSwitch13
from webob import Response
from  ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib import dpid as dpid_lib
from ryu.lib.packet import arp
from network import Host, Honeypot, Subnet, Network
from utils import Utils as u

name = 'rest_controller'
url = '/rest_controller/insert'
sub = '192.168.2.'
ips = []

# ------- NETWORK TOPOLPOGY -------------------------------------------------------------- #
        
# Nodes
host = Host('host', '192.168.2.10', '00:00:00:00:00:03', 3, '255.255.255.0')
heralding = Honeypot('heralding', '192.168.2.40', '00:00:00:00:00:05', 5, '255.255.255.0')
cowrie = Honeypot('cowrie', '192.168.2.20', '00:00:00:00:00:02', 2, '255.255.255.0')
elk = Host('ELK', '192.168.3.30', '00:00:00:00:00:06', 6, '255.255.255.0')

# Subnets
subnet1 = Subnet('S1', '192.168.2.0', '255.255.255.0')
subnet2 = Subnet('S2', '192.168.3.0', '255.255.255.0')
subnet3 = Subnet('S3', '192.168.4.0', '255.255.255.0')

# Network
network = Network('Net')

# Add nodes to subnets
subnet1.add_node(host, host.get_gateway_port())
subnet1.add_node(heralding, heralding.get_gateway_port())
subnet2.add_node(elk, elk.get_gateway_port())
subnet1.add_node(cowrie, cowrie.get_gateway_port())

# Add subnets to network
network.add_subnet(subnet1)
network.add_subnet(subnet2)
network.add_subnet(subnet3)

# -------------------------------------------------------------------------------------- #

class RestController(ExampleSwitch13):
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(RestController, self).__init__(*args, **kwargs)
        self.switches = {}
        wsgi = kwargs['wsgi']
        wsgi.register(SimpleSwitchController,
                      {name: self})
    

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        super(RestController, self).switch_features_handler(ev)
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        self.mac_to_port.setdefault(datapath.id, {})
    
    # Policies
    def drop_arp_req(self, dpid, src_ip):
        datapath = self.switches.get(dpid)   
        parser = datapath.ofproto_parser
        actions = []
        match = parser.OFPMatch(eth_type=0x0806, arp_op=arp.ARP_REQUEST, 
                                arp_spa=src_ip)
        self.add_flow(datapath, 10001, match, actions)
    
    def change_host_src(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        new_ip = u.make_new_IP(ips, sub)
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(arp_spa=new_ip),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0806, arp_op=arp.ARP_REPLY, 
                                arp_spa=heralding.get_ip_addr(), arp_tpa=src_ip)
        self.add_flow(datapath, 10002, match, actions)
    
    def del_prev_rules(self, dpid, mac):
        datapath = self.switches.get(dpid)
        self.del_flow(datapath, mac)

    def redirect_to_cowrie(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionSetField(eth_dst=cowrie.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=cowrie.get_ip_addr()),
                   parser.OFPActionSetField(tcp_dst=23),
                   parser.OFPActionOutput(cowrie.get_gateway_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, 
                                ipv4_dst=heralding.get_ip_addr(), ip_proto=6, tcp_dst=23)
        self.add_flow(datapath, 10003, match, actions)
    
    def change_cowrie_src(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(eth_src=heralding.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=heralding.get_ip_addr()),
                   parser.OFPActionSetField(tcp_src=23),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                ip_proto=6, tcp_src=23)
        self.add_flow(datapath, 10003, match, actions)

class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[name]

    @route('restswitch', '/rest_controller/insert_rule', methods=['POST'])
    def insert_rule(self, req, **kwargs):
        richiesta = req.json
        print(richiesta)
        simple_switch = self.simple_switch_app
        if richiesta:
            dpid = richiesta['dpid']
            #print(dpid)
            match = richiesta['match']
            src = match['nw_src']

            actions = richiesta['actions']
            values = actions[0]
            t = values['type']
            mac = u.host_to_mac(subnet1, src)

            simple_switch.del_prev_rules(dpid, mac)
            #simple_switch.redirect_to_cowrie(dpid, src)
            #simple_switch.change_cowrie_src(dpid, src)
            simple_switch.change_host_src(dpid, src)

            return Response(status=200)
        else:
            return Response(status=400)

    
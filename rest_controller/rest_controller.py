import json

from controller import ExampleSwitch13
from webob import Response
from  ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib import dpid as dpid_lib
from ryu.lib.packet import arp, icmp
from network import Host, Honeypot, Subnet, Network, Gateway
from utils import Utils as u
from randmac import RandMac


name = 'rest_controller'
url = '/rest_controller/insert'
sub = '192.168.3.'
ips = []

# ------- NETWORK TOPOLPOGY -------------------------------------------------------------- #    
# Nodes
host = Host('host', '192.168.3.10', '08:00:27:b6:d0:66', 15, '255.255.255.0')
service = Host('service', '192.168.3.11', '08:00:27:29:bd:84', 3, '255.255.255.0')
heralding = Honeypot('heralding', '192.168.3.12', '08:00:27:0b:8b:8e', 4, '255.255.255.0')

cowrie = Honeypot('cowrie', '192.168.4.10', '08:00:27:e5:e1:01', 6, '255.255.255.0')
heralding1 = Honeypot('heralding1', '192.168.4.11', '08:00:27:f4:0c:20', 13, '255.255.255.0')

elk_if1 = Host('ELK_IF1', '192.168.5.10', '08:00:27:b4:ad:5c', 8, '255.255.255.0')
elk_if2 = Host('ELK_IF2', '192.168.11.10', '08:00:27:13:25:57', 13, '255.255.255.0')

dmz_heralding = Honeypot('dmz_heralding', '192.168.10.10', '08:00:27:9f:12:16', 2, '255.255.255.0')
dmz_service = Host('dmz_service', '192.168.10.11', '08:00:27:b6:d0:67', 22, '255.255.255.0')
dmz_host = Host('dmz_host', '192.168.10.12', '08:00:27:b6:d0:68', 23, '255.255.255.0')

# Subnets
# ovs1
subnet1 = Subnet('S1', '192.168.3.0', '255.255.255.0')
subnet2 = Subnet('S2', '192.168.4.0', '255.255.255.0')
subnet3 = Subnet('S3', '192.168.5.0', '255.255.255.0')
#ovs2
subnet4 = Subnet('S4', '192.168.10.0', '255.255.255.0')
subnet5 = Subnet('S5', '192.168.11.0', '255.255.255.0')

# Gateways
# ovs1
gw1 = Gateway('gw1', '192.168.3.1', '9e:c3:c6:49:0e:e8', 1, '255.255.255.0')
gw2 = Gateway('gw2', '192.168.4.1', '16:67:1f:3f:86:a7', 5, '255.255.255.0')
gw3 = Gateway('gw3', '192.168.5.1', 'fe:46:67:35:0d:d1', 7, '255.255.255.0')
# ovs2
gw10 = Gateway('gw10', '192.168.10.1', '8a:ae:02:40:8f:93', 1, '255.255.255.0')
gw11 = Gateway('gw11', '192.168.11.1', 'ea:6a:20:a0:96:11', 4, '255.255.255.0')

# Network
network1 = Network('Net1')
network2 = Network('Net2')

# Add nodes to subnets
# ovs1
subnet1.add_node(host, host.get_ovs_port())
subnet1.add_node(heralding, heralding.get_ovs_port())
subnet1.add_node(service, service.get_ovs_port())
subnet1.add_node(gw1, gw1.get_ovs_port())

subnet2.add_node(cowrie, cowrie.get_ovs_port())
subnet2.add_node(heralding1, heralding1.get_ovs_port())
subnet2.add_node(gw2, gw2.get_ovs_port())

subnet3.add_node(elk_if1, elk_if1.get_ovs_port())
subnet3.add_node(gw3, gw3.get_ovs_port())

#ovs2
subnet4.add_node(dmz_service, dmz_service.get_ovs_port())
subnet4.add_node(dmz_heralding, dmz_heralding.get_ovs_port())
subnet4.add_node(dmz_host, dmz_host.get_ovs_port())
subnet4.add_node(gw10, gw10.get_ovs_port())

subnet5.add_node(elk_if2, elk_if2.get_ovs_port())
subnet5.add_node(gw11, gw11.get_ovs_port())


# Add subnets to network
network1.add_subnet(subnet1)
network1.add_subnet(subnet2)
network1.add_subnet(subnet3)

network2.add_subnet(subnet4)
network2.add_subnet(subnet5)

ports = [23, 5432, 143, 5900, 3306]

br0_dpid = 85884017520972
br1_dpid = 101737510984148

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


    # # MAC OBFUSCATION
    # def change_host_src(self, dpid, src_ip, ip_item, new_mac):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, src_ip)
    #     src_mac = u.host_to_mac(subnet1, src_ip)
    #     mac_item = u.host_to_mac(subnet1, ip_item)
    #     actions = [parser.OFPActionSetField(arp_sha=new_mac),
    #                parser.OFPActionOutput(out_port)]
    #     match = parser.OFPMatch(eth_type=0x0806, arp_op=arp.ARP_REPLY,
    #                             arp_sha=mac_item, arp_tha=src_mac)
    #     self.add_flow_with_idle(datapath, 1000, match, actions)
    #     #self.add_flow(datapath, 1000, match, actions, 1)

    # def redirect_icmp_request(self, dpid, src_ip, ip_item, new_mac):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, ip_item)
    #     src_mac = u.host_to_mac(subnet1, src_ip)
    #     mac_item = u.host_to_mac(subnet1, ip_item)
    #     actions = [parser.OFPActionSetField(eth_dst=mac_item),
    #                parser.OFPActionOutput(out_port)]
    #     match = parser.OFPMatch(eth_type=0x0800, eth_src=src_mac, eth_dst=new_mac, ip_proto=1,
    #                             icmpv4_type=icmp.ICMP_ECHO_REQUEST)
    #     self.add_flow_with_idle(datapath, 1000, match, actions)
    #     #self.add_flow(datapath, 1000, match, actions, 1)

    # def change_host_icmp_reply(self, dpid, src_ip, ip_item, new_mac):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, src_ip)
    #     src_mac = u.host_to_mac(subnet1, src_ip)
    #     mac_item = u.host_to_mac(subnet1, ip_item)
    #     actions = [parser.OFPActionSetField(eth_src=new_mac),
    #                parser.OFPActionOutput(out_port)]
    #     match = datapath.ofproto_parser.OFPMatch(eth_type=0x800, eth_src=mac_item,
    #                                              eth_dst=src_mac, ip_proto=1, icmpv4_type=icmp.ICMP_ECHO_REPLY)
    #     self.add_flow_with_idle(datapath, 1000, match, actions)
    #     #self.add_flow(datapath, 1000, match, actions, 1)

    # def redirect_tcp_request(self, dpid, src_ip, ip_item, new_mac):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, ip_item)
    #     src_mac = u.host_to_mac(subnet1, src_ip)
    #     mac_item = u.host_to_mac(subnet1, ip_item)
    #     actions = [parser.OFPActionSetField(eth_dst=mac_item),
    #                parser.OFPActionOutput(out_port)]       
    #     match = parser.OFPMatch(eth_type=0x0800, eth_src=src_mac, eth_dst=new_mac, ip_proto=6)
    #     self.add_flow_with_idle(datapath, 1000, match, actions)
    #     #self.add_flow(datapath, 1000, match, actions, 1)
    
    # def change_host_tcp_response(self, dpid, src_ip, ip_item, new_mac):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, src_ip)
    #     src_mac = u.host_to_mac(subnet1, src_ip)
    #     mac_item = u.host_to_mac(subnet1, ip_item)
    #     actions = [parser.OFPActionSetField(eth_src=new_mac),
    #                parser.OFPActionOutput(out_port)]
    #     match = datapath.ofproto_parser.OFPMatch(eth_type=0x800, eth_src=mac_item,
    #                                              eth_dst=src_mac, ip_proto=6)
    #     self.add_flow_with_idle(datapath, 1000, match, actions)
        #self.add_flow(datapath, 1000, match, actions, 1)       
    
    # REDIRECTION TO HERALDING
    def redirect_to_heralding_ftp(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(subnet1, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=heralding1.get_ip_addr()),
                   parser.OFPActionOutput(gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=service.get_ip_addr(), ip_proto=6, tcp_dst=21)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_heralding_src_ftp(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw1.get_MAC_addr(), ip_proto=6, tcp_src=21)                
        self.add_flow(datapath, 1000, match, actions, 1)

    def del_rules_cookie(self, dpid, cookie):
        datapath = self.switches.get(dpid)
        self.del_rules(datapath, cookie)

    # REDIRECTION TO COWRIE CHANGING DEST PORT
    def redirect_to_cowrie_smtp_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionSetField(eth_dst=gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=cowrie.get_ip_addr()),
                   parser.OFPActionSetField(tcp_dst=23),
                   parser.OFPActionOutput(gw1.get_ovs_port())]        
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=service.get_ip_addr(), ip_proto=6, tcp_dst=25)   
        self.add_flow(datapath, 1000, match, actions, 1)

    def change_cowrie_src_smtp_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionSetField(tcp_src=25),
                   parser.OFPActionOutput(out_port)]        
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw1.get_MAC_addr(), ip_proto=6, tcp_src=23)
        self.add_flow(datapath, 1000, match, actions, 1)
       
    # REDIRECTION TO COWRIE
    # Presuppongo che applico il MTD esclusivamente nella subnet1 (rete interna)
    def redirect_to_cowrie_ssh(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=cowrie.get_ip_addr()),
                   parser.OFPActionOutput(gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_ssh(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)
    
    def redirect_to_cowrie_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionSetField(eth_dst=gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=cowrie.get_ip_addr()),
                   parser.OFPActionOutput(gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=service.get_ip_addr(), ip_proto=6, tcp_dst=23)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw1.get_MAC_addr(), ip_proto=6, tcp_src=23)
        self.add_flow(datapath, 1000, match, actions, 2)

    # PORT HOPPING
    def drop_http_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(subnet1, src_ip)
        actions = []
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=80)
        self.add_flow(datapath, 1000, match, actions, 0)

    def redirect_pop3_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser        
        src_mac = u.host_to_mac(subnet1, src_ip)
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 110, datapath)

        actions = [parser.OFPActionSetField(eth_dst=gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=heralding1.get_ip_addr()),
                   parser.OFPActionOutput(gw1.get_ovs_port())]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=110)
        self.add_flow(datapath, 1000, match, actions, 0)

    def change_heralding_src_pop3(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet1, src_ip) 
        actions = [parser.OFPActionSetField(eth_src=service.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw1.get_MAC_addr(), ip_proto=6, tcp_src=110)
        self.add_flow(datapath, 1000, match, actions, 0)



    # def change_http_port(self, dpid, src_ip):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(subnet1, src_ip)
    #     self.port = 110
    #     # PERMIT tcp input to service port 110
    #     self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 110, datapath)
    #     actions = [parser.OFPActionSetField(tcp_src=110),
    #                parser.OFPActionOutput(out_port)]
    #     match = parser.OFPMatch(eth_type=0x0800, ipv4_src=service.get_ip_addr(), ipv4_dst=src_ip, 
    #                             eth_src=service.get_MAC_addr(), ip_proto=6, tcp_src=80)  
    #     self.add_flow(datapath, 1000, match, actions, 0)

    # def drop_pop3_rst(self, dpid, src_ip):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     actions = []
    #     match = parser.OFPMatch(eth_type=0x0800, ipv4_src=service.get_ip_addr(), ipv4_dst=src_ip, 
    #                             eth_src=service.get_MAC_addr(), ip_proto=6, tcp_src=110)   
    #     self.add_flow(datapath, 1000, match, actions, 0)          
                            
    # def send_to_controller(self, dpid, src_ip):
    #     datapath = self.switches.get(dpid)
    #     ofproto = datapath.ofproto
    #     parser = datapath.ofproto_parser
    #     actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
    #                                       ofproto.OFPCML_NO_BUFFER)]
    #     match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=service.get_ip_addr(), 
    #                            ip_proto=6, tcp_dst=self.port)
    #     self.add_flow(datapath, 1000, match, actions, 0)

    # REDIRECTION TO HERALDING FOR DMZ HOST (SERVICE SSH, PORT 22)
    def redirect_to_heralding_ssh(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(subnet1, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=gw10.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=heralding1.get_ip_addr()),
                   parser.OFPActionOutput(gw10.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=dmz_service.get_ip_addr(), ip_proto=6, tcp_dst=22)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_heralding_src_ssh(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(subnet4, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=dmz_service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=dmz_service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=gw10.get_MAC_addr(), ip_proto=6, tcp_src=22)                
        self.add_flow(datapath, 1000, match, actions, 1)

class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[name]

    @route('restswitch', '/rest_controller/redirect_to_cowrie_ssh', methods=['POST'])
    def redirect_to_cowrie_ssh(self, req, **kwargs):
        richiesta = req.json
        print(richiesta)
        simple_switch = self.simple_switch_app
        if richiesta:
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid)

            #simple_switch.del_rules_cookie(dpid, 2)
            simple_switch.redirect_to_cowrie_ssh(dpid, src_IP)
            simple_switch.change_cowrie_src_ssh(dpid, src_IP)
            # simple_switch.redirect_to_cowrie_telnet(dpid, src_IP)
            # simple_switch.change_cowrie_src_telnet(dpid, src_IP)

            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_to_heralding', methods=['POST'])
    def redirect_to_heralding(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid)            
            simple_switch.redirect_to_heralding_ftp(dpid, src_IP)
            simple_switch.change_heralding_src_ftp(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_to_cowrie_smtp_telnet', methods=['POST'])
    def redirect_to_cowrie_smtp_telnet(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid)            
            simple_switch.redirect_to_cowrie_smtp_telnet(dpid, src_IP)
            simple_switch.change_cowrie_src_smtp_telnet(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)

    @route('restswitch', '/rest_controller/http_port_hopping', methods=['POST'])
    def http_port_hopping(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid)       
            simple_switch.drop_http_syn(dpid, src_IP)
            simple_switch.redirect_pop3_syn(dpid, src_IP)
            simple_switch.change_heralding_src_pop3(dpid, src_IP)
     
            #simple_switch.change_http_port(dpid, src_IP)
            #simple_switch.drop_pop3_rst(dpid, src_IP)
            #simple_switch.send_to_controller(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_to_heralding_dmz_ssh', methods=['POST'])
    def redirect_to_heralding_dmz_ssh(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid) 
            simple_switch.redirect_to_heralding_ssh(dpid, src_IP)
            simple_switch.change_heralding_src_ssh(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
        

    @route('restswitch', '/rest_controller/mac_shuffling', methods=['POST'])
    def mac_shuffling(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app
        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            dpid = int(dpid)

            #simple_switch.del_rules_cookie(dpid, 1)

            # for k, v in subnet1.nodes.items():
            #     ip_item = v.get_ip_addr()
            #     if ip_item != src_IP and ip_item != gw1.get_ip_addr():
            #         print(ip_item)
            #         new_mac = RandMac()
            #         new_mac = str(new_mac)
                    # simple_switch.change_host_src(dpid, src_IP, ip_item, new_mac)
                    # simple_switch.redirect_icmp_request(dpid, src_IP, ip_item, new_mac)
                    # simple_switch.change_host_icmp_reply(dpid, src_IP, ip_item, new_mac)
                    # simple_switch.redirect_tcp_request(dpid, src_IP, ip_item, new_mac)
                    # simple_switch.change_host_tcp_response(dpid, src_IP, ip_item, new_mac)
            simple_switch.redirect_to_heralding_ftp(dpid, src_IP)
            simple_switch.change_heralding_src_ftp(dpid, src_IP)

            simple_switch.redirect_to_cowrie_smtp_telnet(dpid, src_IP)
            simple_switch.change_cowrie_src_smtp_telnet(dpid, src_IP)

            simple_switch.change_http_port(dpid, src_IP)
            simple_switch.drop_pop3_rst(dpid, src_IP)

            return Response(status=200)
        else:
            return Response(status=400)
    
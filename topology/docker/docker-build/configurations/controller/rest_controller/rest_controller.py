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
import topology as t
import ti_management as man


name = 'rest_controller'
url = '/rest_controller/insert'
sub = '192.168.3.'
ips = []

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
    
    # REDIRECTION TO HERALDING
    def redirect_to_heralding_ftp(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=21)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_heralding_src_ftp(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=t.service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=21)                
        self.add_flow(datapath, 1000, match, actions, 1)

    def del_rules_cookie(self, dpid, cookie):
        datapath = self.switches.get(dpid)
        self.del_rules(datapath, cookie)

    # REDIRECTION TO COWRIE CHANGING DEST PORT
    # def redirect_to_cowrie_telnet(self, dpid, src_ip):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
    #                parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
    #                parser.OFPActionOutput(t.gw1.get_ovs_port())]        
    #     match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
    #                             ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=23)   
    #     self.add_flow(datapath, 1000, match, actions, 1)

    # def change_cowrie_src_telnet(self, dpid, src_ip):
    #     datapath = self.switches.get(dpid)
    #     parser = datapath.ofproto_parser
    #     out_port = u.host_to_port(t.subnet1, src_ip)
    #     actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
    #                parser.OFPActionOutput(out_port)]        
    #     match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
    #                             eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=23)
    #     self.add_flow(datapath, 1000, match, actions, 1)
       
    # REDIRECTION TO COWRIE
    # Presuppongo che applico il MTD esclusivamente nella subnet1 (rete interna)
    def redirect_to_cowrie_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)
    

    def redirect_to_cowrie_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.ssh_service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.ssh_service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)


    
    def redirect_to_cowrie_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=23)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_cowrie_src_telnet(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=23)
        self.add_flow(datapath, 1000, match, actions, 2)
    
    # REDIRECT TO HERALDING SSH - FROM INTERNAL NETWORK
    def redirect_to_heralding_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_heralding_src_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)   



    def redirect_to_heralding_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        self.attacker = src_ip
        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.ssh_service.get_ip_addr(), ip_proto=6, tcp_dst=22)
        self.add_flow(datapath, 1000, match, actions, 2)

    def change_heralding_src_ssh_int_dup(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.ssh_service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)   


    def change_heralding_src_ssh_int(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=22)
        self.add_flow(datapath, 1000, match, actions, 2)     

    # PORT HOPPING
    def drop_http_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet1, src_ip)
        actions = []
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=t.service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=80)
        self.add_flow(datapath, 1000, match, actions, 0)

    def redirect_socks5_syn(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser        
        src_mac = u.host_to_mac(t.subnet1, src_ip)
        self.permit_tcp_dstIP_dstPORT(parser, t.service.get_ip_addr(), t.service.get_ovs_port(), 1080, datapath)

        actions = [parser.OFPActionSetField(eth_dst=t.gw1.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw1.get_ovs_port())]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=t.service.get_ip_addr(), 
                                eth_src=src_mac, ip_proto=6, tcp_dst=1080)
        self.add_flow(datapath, 1000, match, actions, 0)

    def change_heralding_src_socks5(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet1, src_ip) 
        actions = [parser.OFPActionSetField(eth_src=t.service.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=t.service.get_ip_addr()),
                   parser.OFPActionOutput(out_port)]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw1.get_MAC_addr(), ip_proto=6, tcp_src=1080)
        self.add_flow(datapath, 1000, match, actions, 0)


    # REDIRECTION TO HERALDING FOR DMZ HOST (SERVICE SSH, PORT 22)
    def redirect_to_heralding_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=t.gw10.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.heralding1.get_ip_addr()),
                   parser.OFPActionOutput(t.gw10.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.dmz_service.get_ip_addr(), ip_proto=6, tcp_dst=22)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_heralding_src_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.dmz_service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=t.dmz_service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.heralding1.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw10.get_MAC_addr(), ip_proto=6, tcp_src=22)                
        self.add_flow(datapath, 1000, match, actions, 1)
    
    # REDIRECT TO COWRIE FROM DMZ HOST (SERVICE SSH, PORT 22)
    def redirect_to_cowrie_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        src_mac = u.host_to_mac(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(eth_dst=t.gw10.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=t.cowrie.get_ip_addr()),
                   parser.OFPActionOutput(t.gw10.get_ovs_port())]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip,
                                ipv4_dst=t.dmz_service.get_ip_addr(), ip_proto=6, tcp_dst=22)              
        self.add_flow(datapath, 1000, match, actions, 1)
    
    def change_cowrie_src_ssh_ext(self, dpid, src_ip):
        datapath = self.switches.get(dpid)
        parser = datapath.ofproto_parser
        out_port = u.host_to_port(t.subnet4, src_ip)
        actions = [parser.OFPActionSetField(ipv4_src=t.dmz_service.get_ip_addr()),
                   parser.OFPActionSetField(eth_src=t.dmz_service.get_MAC_addr()),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=t.cowrie.get_ip_addr(), ipv4_dst=src_ip, 
                                eth_src=t.gw10.get_MAC_addr(), ip_proto=6, tcp_src=22)                
        self.add_flow(datapath, 1000, match, actions, 1)   

class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[name]

    @route('restswitch', '/rest_controller/redirect_ssh_int', methods=['POST'])
    def redirect_to_cowrie_ssh(self, req, **kwargs):
        richiesta = req.json
        print(richiesta)
        simple_switch = self.simple_switch_app
        if richiesta:
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            #dpid = int(dpid)
            dpid = t.br0_dpid

            a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
            b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

            # default = redirect to cowrie
            # if cowrie is busy redirect to heralding
            if (a and b) == 0: 
                man.sb[man.COWRIE_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_cowrie_ssh_int(dpid, src_IP)
                simple_switch.change_cowrie_src_ssh_int(dpid, src_IP)
            else:
                man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_heralding_ssh_int(dpid, src_IP)
                simple_switch.change_heralding_src_ssh_int(dpid, src_IP)

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
            #dpid = int(dpid)     
            dpid = t.br0_dpid   
            man.sb[man.HERALDING_INDEX][man.FTP_INDEX] = 1    
            simple_switch.redirect_to_heralding_ftp(dpid, src_IP)
            simple_switch.change_heralding_src_ftp(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_to_cowrie_telnet', methods=['POST'])
    def redirect_to_cowrie_telnet(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            #dpid = int(dpid)    
            dpid = t.br0_dpid
            man.sb[man.COWRIE_INDEX][man.TELNET_INDEX] = 1     
            simple_switch.redirect_to_cowrie_telnet(dpid, src_IP)
            simple_switch.change_cowrie_src_telnet(dpid, src_IP)
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
            #dpid = int(dpid)       
            dpid = t.br0_dpid
            man.sb[man.HERALDING_INDEX][man.SOCKS5_INDEX] = 1
            simple_switch.drop_http_syn(dpid, src_IP)
            simple_switch.redirect_socks5_syn(dpid, src_IP)
            simple_switch.change_heralding_src_socks5(dpid, src_IP)
     
            #simple_switch.change_http_port(dpid, src_IP)
            #simple_switch.drop_pop3_rst(dpid, src_IP)
            #simple_switch.send_to_controller(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
    
    @route('restswitch', '/rest_controller/redirect_ssh_dmz', methods=['POST'])
    def redirect_to_heralding_dmz_ssh(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app

        if richiesta:
            print(richiesta)
            dpid = richiesta['Dpid']
            src_IP = richiesta['Source_IP']
            #dpid = int(dpid) 
            dpid = t.br1_dpid
            a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
            b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

            if (a and b) == 0: 
                man.sb[man.COWRIE_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_cowrie_ssh_ext(dpid, src_IP)
                simple_switch.change_cowrie_src_ssh_ext(dpid, src_IP)
            else:           
                man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_heralding_ssh_ext(dpid, src_IP)
                simple_switch.change_heralding_src_ssh_ext(dpid, src_IP)
            return Response(status=200)
        else:
            return Response(status=400)
        

    @route('restswitch', '/rest_controller/push_int_server_out', methods=['POST'])
    def push_int_server_out(self, req, **kwargs):
            richiesta = req.json
            simple_switch = self.simple_switch_app
            if richiesta:
                print(richiesta)
                src_IP = richiesta['Source_IP']
                #dpid = int(dpid) 
                dpid = t.br0_dpid

                a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
                b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

                #if (a and b) == 0: 
                man.sb[man.COWRIE_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_cowrie_ssh_int_dup(dpid, src_IP)
                simple_switch.change_cowrie_src_ssh_int_dup(dpid, src_IP)
                #else:           
                    #man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                    #simple_switch.redirect_to_heralding_ssh_int_dup(dpid, src_IP)
                    #simple_switch.change_heralding_src_ssh_int_dup(dpid, src_IP)
                return Response(status=200)
            else:
                return Response(status=400)
            
    @route('restswitch', '/rest_controller/push_dmz_server_out', methods=['POST'])
    def push_dmz_server_out(self, req, **kwargs):
            richiesta = req.json
            simple_switch = self.simple_switch_app
            if richiesta:
                print(richiesta)
                src_IP = richiesta['Source_IP']
                #dpid = int(dpid) 
                dpid = t.br1_dpid

                a = man.sm[man.COWRIE_INDEX][man.SSH_INDEX]
                b = man.sb[man.COWRIE_INDEX][man.SSH_INDEX]

                #if (a and b) == 0: 
                man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                simple_switch.redirect_to_heralding_ssh_ext(dpid, src_IP)
                simple_switch.change_heralding_src_ssh_ext(dpid, src_IP)
                #else:           
                    #man.sb[man.HERALDING_INDEX][man.SSH_INDEX] = 1
                    #simple_switch.redirect_to_heralding_ssh_int_dup(dpid, src_IP)
                    #simple_switch.change_heralding_src_ssh_int_dup(dpid, src_IP)
                return Response(status=200)
            else:
                return Response(status=400)
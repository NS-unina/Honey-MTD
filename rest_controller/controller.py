# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from utils import Utils as u
from network import Host, Honeypot, Attacker, Subnet, Network, Gateway
from ryu.lib.packet import tcp, icmp, arp, ipv4, vlan
import random

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

class ExampleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
        self.mac_to_ip = {}
        self.port = None
        self.attacker = None

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id

        if dpid == br0_dpid:
            print(dpid)
            self.port = ports[random.randint(0, 4)]
            # install the table-miss flow entry.
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                            ofproto.OFPCML_NO_BUFFER)]
            #self.send_set_async(datapath)
            self.add_flow(datapath, 0, match, actions, 0)
            self.add_default_rules_br0(datapath)
        
        if dpid == br1_dpid:
            # install the table-miss flow entry
            print(dpid)
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 0, match, actions, 0)
            self.add_default_rules_br1(datapath)
            
    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id


        if dpid == br0_dpid:
            if msg.cookie == 4:
                values = msg.match.items()
                print(values)
                ipv4_dst = values[1][1]
                port_dst = values[3][1]
                self.drop_tcp_dstIP_dstPORT(parser, ipv4_dst, port_dst, datapath) 
            
                self.port = ports[random.randint(0, 4)]
                self.redirect_protocol_syn(parser, datapath, self.port)
                self.change_heralding_src_protocol(parser, datapath, self.port)
        
        if dpid == br1_dpid:
            pass
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']
        out_port = ofproto.OFPP_FLOOD

        if dpid == br0_dpid:
            if dst == host.get_MAC_addr():
                out_port = host.get_ovs_port()
            elif dst == service.get_MAC_addr():
                out_port = service.get_ovs_port()
            elif dst == heralding.get_MAC_addr():
                out_port = heralding.get_ovs_port()
            elif dst == gw1.get_MAC_addr():
                out_port = gw1.get_ovs_port()
            elif dst == cowrie.get_MAC_addr():
                out_port = cowrie.get_ovs_port()
            elif dst == gw2.get_MAC_addr():
                out_port = gw2.get_ovs_port()
            elif dst == elk_if1.get_MAC_addr():
                out_port = elk_if1.get_ovs_port()
            elif dst == gw3.get_MAC_addr():
                out_port = gw3.get_ovs_port()


            actions = [parser.OFPActionOutput(out_port)]

            # install a flow to avoid packet_in next time.
            if out_port != ofproto.OFPP_FLOOD:
                match = parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions, 0)

            # construct packet_out message and send it.
            out = parser.OFPPacketOut(datapath=datapath,
                                    buffer_id=ofproto.OFP_NO_BUFFER,
                                    in_port=in_port, actions=actions,
                                    data=msg.data)
            datapath.send_msg(out)

        if dpid == br1_dpid:
            if dst == dmz_service.get_MAC_addr():
                out_port = dmz_service.get_ovs_port()
            elif dst == dmz_heralding.get_MAC_addr():
                out_port = dmz_heralding.get_ovs_port()
            elif dst == dmz_host.get_MAC_addr():
                out_port = dmz_host.get_ovs_port()
            elif dst == gw10.get_MAC_addr():
                out_port = gw10.get_ovs_port()
            elif dst == elk_if2.get_MAC_addr():
                out_port = elk_if2.get_ovs_port()
            elif dst == gw11.get_MAC_addr():
                out_port = gw11.get_ovs_port()

            actions = [parser.OFPActionOutput(out_port)]

            # install a flow to avoid packet_in next time.
            if out_port != ofproto.OFPP_FLOOD:
                match = parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions, 0)

            # construct packet_out message and send it.
            out = parser.OFPPacketOut(datapath=datapath,
                                    buffer_id=ofproto.OFP_NO_BUFFER,
                                    in_port=in_port, actions=actions,
                                    data=msg.data)
            datapath.send_msg(out)

    # UTILITY FUNCTIONS
    def add_flow(self, datapath, priority, match, actions, cookie):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, cookie=cookie,
                                match=match, instructions=inst, idle_timeout=0, 
                                hard_timeout=0)
        datapath.send_msg(mod)

    def add_flow_with_hard(self, datapath, priority, match, actions, cookie):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, cookie=cookie,
                                match=match, instructions=inst, flags=ofproto.OFPFF_SEND_FLOW_REM, idle_timeout=0, hard_timeout=20)
        datapath.send_msg(mod)

    def del_rules(self, datapath, cookie, match):
        ofproto = datapath.ofproto
        inst = []
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, ofproto.OFPTT_ALL,
                                                      ofproto.OFPFC_DELETE, 0, 0,
                                                      0,
                                                      ofproto.OFPCML_NO_BUFFER,
                                                      ofproto.OFPP_ANY,
                                                      ofproto.OFPG_ANY, 0,
                                                      match, inst)
        datapath.send_msg(flow_mod)

    def add_default_rules_br0(self, datapath):
        parser = datapath.ofproto_parser
        self.drop_arp_srcIP_srcMAC(parser, gw1.get_ip_addr(), gw2.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw1.get_ip_addr(), gw3.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw1.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw1.get_ip_addr(), gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, gw1.get_ip_addr(), gw11.get_MAC_addr(), datapath, 2) 

        self.drop_arp_srcIP_srcMAC(parser, gw2.get_ip_addr(), gw1.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw2.get_ip_addr(), gw3.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw2.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw2.get_ip_addr(), gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, gw2.get_ip_addr(), gw11.get_MAC_addr(), datapath, 2)

        self.drop_arp_srcIP_srcMAC(parser, gw3.get_ip_addr(), gw1.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw3.get_ip_addr(), gw2.get_MAC_addr(), datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw3.get_ip_addr(), '5c:87:9c:33:d9:d4', datapath, 2)
        self.drop_arp_srcIP_srcMAC(parser, gw3.get_ip_addr(), gw10.get_MAC_addr(), datapath, 2)        
        self.drop_arp_srcIP_srcMAC(parser, gw3.get_ip_addr(), gw11.get_MAC_addr(), datapath, 2)


        # DROP host to elk
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, host.get_ip_addr(), host.get_MAC_addr(), 
                                         elk_if1.get_ip_addr(), datapath)
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, host.get_ip_addr(), host.get_MAC_addr(), 
                                         elk_if1.get_ip_addr(), datapath)
        
        # DROP host to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, host.get_ip_addr(), host.get_MAC_addr(), 
                                         '192.168.5.100', datapath)      
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, host.get_ip_addr(), host.get_MAC_addr(), 
                                         '192.168.5.100', datapath)  
             
        # DROP service to elk
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, service.get_ip_addr(), service.get_MAC_addr(), 
                                         elk_if1.get_ip_addr(), datapath)        
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, service.get_ip_addr(), service.get_MAC_addr(), 
                                         elk_if1.get_ip_addr(), datapath)    
           
        # DROP service to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, service.get_ip_addr(), service.get_MAC_addr(), 
                                         '192.168.5.100', datapath)
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, service.get_ip_addr(), service.get_MAC_addr(), 
                                         '192.168.5.100', datapath)    
           
        # DROP heralding to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, heralding.get_ip_addr(), heralding.get_MAC_addr(), 
                                         '192.168.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, heralding.get_ip_addr(), heralding.get_MAC_addr(), 
                                         '192.168.5.100', datapath)  
        
        # DROP cowrie to controller    
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, cowrie.get_ip_addr(), cowrie.get_MAC_addr(), 
                                         '192.168.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, cowrie.get_ip_addr(), cowrie.get_MAC_addr(), 
                                         '192.168.5.100', datapath)
        
        # DROP heralding1 to controller
        self.drop_icmp_srcIP_srcMAC_dstIP(parser, heralding1.get_ip_addr(), heralding1.get_MAC_addr(), 
                                         '192.168.5.100', datapath)    
        self.drop_tcp_srcIP_srcMAC_dstIP(parser, heralding1.get_ip_addr(), heralding1.get_MAC_addr(), 
                                         '192.168.5.100', datapath)          

        # DROP arp input to service
        self.drop_tcp_dstIP(parser, service.get_ip_addr(), datapath)

        # PERMIT tcp input to service port 22
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 22, datapath)

        # PERMIT tcp input to service port 25
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 25, datapath)

        # PERMIT tcp input to service port 80
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 80, datapath)

        # PERMIT tcp input to service port 21
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), 21, datapath)

        # DROP arp input to heralding
        self.drop_tcp_dstIP(parser, heralding.get_ip_addr(), datapath)

        # PERMIT tcp input from service to heralding
        self.permit_tcp_host1_host2(parser, service.get_ip_addr(), heralding.get_ip_addr(), heralding.get_ovs_port(), datapath)
        # PERMIT tcp input from gateway and elk to heralding
        self.permit_tcp_host1_host2(parser, gw1.get_ip_addr(), heralding.get_ip_addr(), heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, elk_if1.get_ip_addr(), heralding.get_ip_addr(), heralding.get_ovs_port(), datapath)
        self.permit_tcp_host1_host2(parser, elk_if1.get_ip_addr(), dmz_heralding.get_ip_addr(), dmz_heralding.get_ovs_port(), datapath)

        # PERMIT tcp input to heralding port 25
        self.permit_tcp_dstIP_dstPORT(parser, heralding.get_ip_addr(), heralding.get_ovs_port(), 25, datapath)

        # DROP arp input to cowrie
        self.drop_tcp_dstIP(parser, cowrie.get_ip_addr(), datapath)

        # PERMIT tcp input to cowrie port 22
        self.permit_tcp_dstIP_dstPORT(parser, cowrie.get_ip_addr(), cowrie.get_ovs_port(), 22, datapath)

        # PERMIT tcp input to cowrie port 23
        self.permit_tcp_dstIP_dstPORT(parser, cowrie.get_ip_addr(), cowrie.get_ovs_port(), 23, datapath)

        # # PERMIT level2 traffic through vlan1
        # self.permit_eth_dstMAC(parser, gw1.get_MAC_addr(), gw1.get_ovs_port(), datapath)

        # # PERMIT level2 traffico thorugh vlan2
        # self.permit_eth_dstMAC(parser, gw2.get_MAC_addr(), gw2.get_ovs_port(), datapath)

        # MTD PROACTIVE PORT SHUFFLING
        self.redirect_protocol_syn(parser, datapath, self.port)
        self.change_heralding_src_protocol(parser, datapath, self.port)

    def add_default_rules_br1(self, datapath):
        parser = datapath.ofproto_parser

        self.drop_icmp_srcIP_srcPORT_dstIP(parser, gw11.get_ip_addr(), 4, '192.168.11.100', datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, gw11.get_ip_addr(), 4, '192.168.11.100', datapath)

        self.drop_icmp_srcIP_srcPORT_dstIP(parser, dmz_service.get_ip_addr(), 22, '192.168.11.100', datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, dmz_service.get_ip_addr(), 22, '192.168.11.100', datapath)

        self.drop_icmp_host1_host2(parser, host.get_ip_addr(), elk_if2.get_ip_addr(), datapath)
        self.drop_tcp_host1_host2(parser, host.get_ip_addr(), elk_if2.get_ip_addr(), datapath)
        self.drop_icmp_srcIP_srcPORT_dstIP(parser, dmz_service.get_ip_addr(), 22, elk_if2.get_ip_addr(), datapath)
        self.drop_tcp_srcIP_srcPORT_dstIP(parser, dmz_service.get_ip_addr(), 22, elk_if2.get_ip_addr(), datapath)


    def send_set_async(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        packet_in_mask = 1 << ofp.OFPR_ACTION | 1 << ofp.OFPR_INVALID_TTL | 1 << ofp.OFPR_NO_MATCH
        port_status_mask = (1 << ofp.OFPPR_ADD
                            | 1 << ofp.OFPPR_DELETE
                            | 1 << ofp.OFPPR_MODIFY)
        flow_removed_mask = (1 << ofp.OFPRR_IDLE_TIMEOUT
                            | 1 << ofp.OFPRR_HARD_TIMEOUT
                            | 1 << ofp.OFPRR_DELETE
                            | 1 << ofp.OFPRR_GROUP_DELETE)

        req = ofp_parser.OFPSetAsync(datapath,
                                    [packet_in_mask, packet_in_mask],
                                    [port_status_mask, port_status_mask],
                                    [flow_removed_mask, flow_removed_mask])
        datapath.send_msg(req)

    def permit_eth_dstMAC(self, parser, eth_dst, ovs_port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_dst=eth_dst)
        self.add_flow(datapath, 200, match, actions, 0)

    def drop_arp_srcIP_srcMAC(self, parser, arp_spa, arp_sha, datapath, op_code):
        '''drop_arp'''
        actions = []
        match = parser.OFPMatch(
            eth_type=0x0806, arp_op=op_code, arp_spa=arp_spa, arp_sha=arp_sha)
        self.add_flow(datapath, 100, match, actions, 0)

    def drop_icmp_srcIP_srcMAC_dstIP(self, parser, ipv4_src, eth_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, eth_src=eth_src, ipv4_dst=ipv4_dst,
            ip_proto=1)
        self.add_flow(datapath, 100, match, actions, 0)    
    
    def drop_icmp_srcIP_srcPORT_dstIP(self, parser, ipv4_src, port_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, in_port=port_src, ipv4_dst=ipv4_dst,
            ip_proto=1)     
        self.add_flow(datapath, 100, match, actions, 0)     

    def drop_tcp_srcIP_srcMAC_dstIP(self, parser, ipv4_src, eth_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, eth_src=eth_src, ipv4_dst=ipv4_dst,
            ip_proto=6)
        self.add_flow(datapath, 100, match, actions, 0)   

    def drop_tcp_srcIP_srcPORT_dstIP(self, parser, ipv4_src, port_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_src, in_port=port_src, ipv4_dst=ipv4_dst,
            ip_proto=6)     
        self.add_flow(datapath, 100, match, actions, 0)   
    
    def drop_tcp_dstIP(self, parser, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=ipv4_dst, ip_proto=6)
        self.add_flow(datapath, 100, match, actions, 0)

    def permit_tcp_host1_host2(self, parser, ipv4_src, ipv4_dst, ovs_port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=6)  
        self.add_flow(datapath, 300, match, actions, 0) 

    def permit_tcp_dstIP_dstPORT(self, parser, ipv4_dst, ovs_port_dest, port_dest, datapath):
        actions = [parser.OFPActionOutput(ovs_port_dest)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_dst=ipv4_dst, tcp_dst=port_dest, ip_proto=6)  
        self.add_flow(datapath, 200, match, actions, 0) 
    
    def drop_tcp_dstIP_dstPORT(self, parser, ipv4_dst, port_dest, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_dst=ipv4_dst, tcp_dst=port_dest, ip_proto=6)
        self.add_flow(datapath, 200, match, actions, 0)
    
    def drop_icmp_host1_host2(self, parser, ipv4_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=1)
        self.add_flow(datapath, 300, match, actions, 0)       

    def drop_tcp_host1_host2(self, parser, ipv4_src, ipv4_dst, datapath):
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_src, ipv4_dst=ipv4_dst, ip_proto=6)
        self.add_flow(datapath, 300, match, actions, 0)  

    # PROACTIVE MTD PORT HOPPING
    def redirect_protocol_syn(self, parser, datapath, port):  
        self.permit_tcp_dstIP_dstPORT(parser, service.get_ip_addr(), service.get_ovs_port(), port, datapath)
        
        actions = [parser.OFPActionSetField(eth_dst=heralding.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_dst=heralding.get_ip_addr()),
                   parser.OFPActionOutput(heralding.get_ovs_port())]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=service.get_ip_addr(), ip_proto=6, tcp_dst=port)
        self.add_flow_with_hard(datapath, 1000, match, actions, 4)

    def change_heralding_src_protocol(self, parser, datapath, port):
        ofproto = datapath.ofproto
        actions = [parser.OFPActionSetField(eth_src=service.get_MAC_addr()),
                   parser.OFPActionSetField(ipv4_src=service.get_ip_addr()),
                   parser.OFPActionOutput(ofproto.OFPP_NORMAL)]       
        match = parser.OFPMatch(eth_type=0x0800, ipv4_src=heralding.get_ip_addr(), 
                                eth_src=heralding.get_MAC_addr(), ip_proto=6, tcp_src=port)
        self.add_flow_with_hard(datapath, 1000, match, actions, 5)
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
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from utils import Utils as u
from network import Host, Honeypot, Attacker, Subnet, Network


class ExampleSwitch13(app_manager.RyuApp):
    '''ExampleSwitch13'''
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
        # initialize forwarding table.
        self.src_ip_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        '''switch_features:handler'''
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        '''add_flow'''
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        datap = msg.data

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.src_ip_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)

        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

# -----------------------------------------------------------------------#
        attacker = Attacker("h10", '192.168.2.10',
                            '00:00:00:00:00:03', 3, '255.255.255.0')
        honeypot = Honeypot("h200", '192.168.2.20',
                            '00:00:00:00:00:02', 2, '255.255.255.0', 'LI')

        #h11 = Host("h11", '200.0.0.101', '00:00:00:00:00:01', 2, '255.255.255.0')
        h12 = Host("h12", '192.168.2.12', '00:00:00:00:00:04', 4, '255.255.255.0')
        h13 = Host("h13", '192.168.2.13', '00:00:00:00:00:05', 5, '255.255.255.0')

        #h20 = Host("h20", '10.0.2.20', '00:00:00:00:00:04', 4, '255.255.255.0')

        subnet1 = Subnet("s1", '192.168.2.0', '255.255.255.0')
        #subnet2 = Subnet("s2", '10.0.2.0', '255.255.255.0')

        subnet1.add_node(attacker, attacker.get_gateway_port())
        subnet1.add_node(honeypot, honeypot.get_gateway_port())
        subnet1.add_node(h11, h11.get_gateway_port())
        subnet1.add_node(h12, h12.get_gateway_port())
        subnet1.add_node(h13, h13.get_gateway_port())

        #subnet2.add_node(h20, h20.get_gateway_port())

        real_network = Network("r_network")
        real_network.add_subnet(subnet1)
        #real_network.add_subnet(subnet2)

# ----------------------------------------------------------------------#
        # Packets
        arp_pkt = pkt.get_protocol(arp.arp)
        icmp_pkt = pkt.get_protocol(icmp.icmp)
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        udp_pkt = pkt.get_protocol(udp.udp)
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)

        
        if arp_pkt:
            op_code = arp_pkt.opcode
            # Attacker
            # Drop if destination is h11
            if op_code == arp.ARP_REQUEST and arp_pkt.src_ip == attacker.get_ip_addr():
                if arp_pkt.dst_ip == h11.get_ip_addr():
                     actions = []
                     self.drop_arp(parser, arp_pkt, datapath, op_code)
            # h11
            if op_code == arp.ARP_REPLY and arp_pkt.src_ip == h11.get_ip_addr():
                if arp_pkt.dst_ip == attacker.get_ip_addr():
                    actions = []
                    self.drop_arp(parser, arp_pkt, datapath, op_code)

            # Drop if destination is honeypot
            if op_code == arp.ARP_REQUEST and arp_pkt.src_ip == attacker.get_ip_addr():
                if arp_pkt.dst_ip == honeypot.get_ip_addr():
                    actions = []
                    self.drop_arp(parser, arp_pkt, datapath, op_code)

            # Permit if destination is host h12 or host h13
            if op_code == arp.ARP_REQUEST and arp_pkt.src_ip == attacker.get_ip_addr():
                
                if (arp_pkt.dst_ip == h12.get_ip_addr() or arp_pkt.dst_ip == h13.get_ip_addr()):
                    out_port = u.host_to_port(subnet1, arp_pkt.dst_ip)
                    actions = [parser.OFPActionOutput(out_port)]
                    self.permit_arp(parser, arp_pkt, datapath,
                                    op_code, out_port)

            # Other hosts
            # Drop if destination is honeypot
            if op_code == arp.ARP_REQUEST and (arp_pkt.src_ip == h11.get_ip_addr() or arp_pkt.src_ip == h12.get_ip_addr() or arp_pkt.src_ip == h13.get_ip_addr()):
                if arp_pkt.dst_ip == honeypot.get_ip_addr():
                    actions = []
                    self.drop_arp(parser, arp_pkt, datapath, op_code)
            if op_code == arp.ARP_REPLY and (arp_pkt.dst_ip == h11.get_ip_addr() or arp_pkt.dst_ip == h12.get_ip_addr() or arp_pkt.dst_ip == h13.get_ip_addr()):
                if arp_pkt.src_ip == honeypot.get_ip_addr():
                    actions = []
                    self.drop_arp(parser, arp_pkt, datapath, op_code)

            # Permit if destination is another host in the subnet
            if (op_code == arp.ARP_REQUEST or op_code == arp.ARP_REPLY) and (arp_pkt.src_ip == h11.get_ip_addr() or arp_pkt.src_ip == h12.get_ip_addr() or arp_pkt.src_ip == h13.get_ip_addr()):
                if (arp_pkt.dst_ip == h11.get_ip_addr() or arp_pkt.dst_ip == h12.get_ip_addr() or arp_pkt.dst_ip == h13.get_ip_addr()):
                    out_port = u.host_to_port(subnet1, arp_pkt.dst_ip)
                    actions = [parser.OFPActionOutput(out_port)]
                    self.permit_arp(parser, arp_pkt, datapath,
                                    op_code, out_port)
        
        if icmp_pkt:

           # Attacker
           # Drops ICMP echo request from attacker to h11 and h12
            if icmp_pkt.type == icmp.ICMP_ECHO_REQUEST and ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h11.get_ip_addr() or ipv4_pkt.dst == h12.get_ip_addr():
                    actions = []
                    self.drop_icmp(parser, ipv4_pkt, datapath, icmp_pkt.type)

           # Redirect to honeypot if echo request is from attacker to h13
            if icmp_pkt.type == icmp.ICMP_ECHO_REQUEST and ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h13.get_ip_addr():
                    self.logger.info("Mi è arrivato 1")
                    actions = [parser.OFPActionSetField(eth_dst=honeypot.get_MAC_addr()),
                               parser.OFPActionSetField(
                                   ipv4_dst=honeypot.get_ip_addr()),
                               parser.OFPActionOutput(honeypot.get_gateway_port())]
                    self.redirect_icmp_echo_request(parser, ipv4_pkt, datapath, honeypot.get_gateway_port(
                    ), honeypot.get_MAC_addr(), honeypot.get_ip_addr(), icmp_pkt.type)

           # Permit ICMP echo request from attacker to honeypot
            if icmp_pkt.type == icmp.ICMP_ECHO_REQUEST and ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == honeypot.get_ip_addr():
                    actions = [parser.OFPActionOutput(
                        honeypot.get_gateway_port())]
                    self.permit_icmp(parser, ipv4_pkt, datapath,
                                     honeypot.get_gateway_port(), icmp_pkt.type)

           # Other hosts
           # Drops ICMP echo request from h11, h12 and h13 to attacker
            if icmp_pkt.type == icmp.ICMP_ECHO_REQUEST and (ipv4_pkt.src == h11.get_ip_addr() or ipv4_pkt.src == h12.get_ip_addr() or ipv4_pkt.src == h13.get_ip_addr()):
                if ipv4_pkt.dst == attacker.get_ip_addr():
                    actions = []
                    self.drop_icmp(parser, ipv4_pkt, datapath, icmp_pkt.type)

           # Permit if destination is another host in the subnet
            if (icmp_pkt.type == icmp.ICMP_ECHO_REQUEST or icmp_pkt.type == icmp.ICMP_ECHO_REPLY) and (ipv4_pkt.src == h11.get_ip_addr() or ipv4_pkt.src == h12.get_ip_addr() or ipv4_pkt.src == h13.get_ip_addr()):
                if (ipv4_pkt.dst == h11.get_ip_addr() or ipv4_pkt.dst == h12.get_ip_addr() or ipv4_pkt.dst == h13.get_ip_addr()):
                    out_port = u.host_to_port(subnet1, ipv4_pkt.dst)
                    actions = [parser.OFPActionOutput(out_port)]
                    self.permit_icmp(parser, ipv4_pkt, datapath,
                                     out_port, icmp_pkt.type)

           # Honeypot
           # If response cames from honeypot to attacker(fagli credere che
           # la risposta proviene da h13)
            if icmp_pkt.type == icmp.ICMP_ECHO_REPLY and ipv4_pkt.src == honeypot.get_ip_addr():
                if ipv4_pkt.dst == attacker.get_ip_addr():
                    self.logger.info("Mi è arrivata la reply")
                    actions = [parser.OFPActionSetField(eth_src=h13.get_MAC_addr()),
                               parser.OFPActionSetField(
                                   ipv4_src=h13.get_ip_addr()),
                               parser.OFPActionOutput(attacker.get_gateway_port())]
                    self.change_icmp_src(parser, ipv4_pkt, datapath, attacker.get_gateway_port(
                    ),  h13.get_MAC_addr(), h13.get_ip_addr(), icmp_pkt.type)

        if tcp_pkt:

            # Attacker
            # Drop if destination of SYN or ACK is host h12
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h12.get_ip_addr():
                    actions = []
                    self.drop_tcp(parser, ipv4_pkt, datapath)

            # Permit if destination of SYN or ACK is honeypot
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == honeypot.get_ip_addr():
                    actions = [parser.OFPActionOutput(
                        honeypot.get_gateway_port())]
                    self.permit_tcp(parser, ipv4_pkt,
                                    datapath, honeypot.get_gateway_port())

            # Redirect to port 8080 of honeypot if destination of SYN or ACK is host h13
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h13.get_ip_addr():
                    if tcp_pkt.dst_port == 23 or tcp_pkt.dst_port == 22:
                        actions = [parser.OFPActionSetField(eth_dst=honeypot.get_MAC_addr()),
                                parser.OFPActionSetField(
                                    ipv4_dst=honeypot.get_ip_addr()),
                                parser.OFPActionSetField(tcp_dst=tcp_pkt.dst_port),
                                parser.OFPActionOutput(honeypot.get_gateway_port())]
                        self.redirect_tcp(parser, ipv4_pkt, datapath, honeypot.get_gateway_port(), honeypot.get_MAC_addr(), honeypot.get_ip_addr(), tcp_pkt.dst_port)
          
                    
            # Honeypot
            # If response cames from honeypot to attacker(fagli credere che
            # la risposta proviene da h13 e quindi la porta 80 di h13 risulta essere open)
            if ipv4_pkt.src == honeypot.get_ip_addr():
                if ipv4_pkt.dst == attacker.get_ip_addr():
                    if tcp_pkt.src_port == 23 or tcp_pkt.src_port == 22:
                        actions = [parser.OFPActionSetField(eth_src=h13.get_MAC_addr()),
                                parser.OFPActionSetField(
                                    ipv4_src=h13.get_ip_addr()),
                                parser.OFPActionSetField(tcp_src=tcp_pkt.src_port),
                                parser.OFPActionOutput(attacker.get_gateway_port())]
                        self.change_tcp_src(parser, ipv4_pkt, datapath,
                                            attacker.get_gateway_port(), h13.get_MAC_addr(), h13.get_ip_addr(), tcp_pkt.src_port)

            # Other hosts
            # Permit comunications tra di loro
            if ipv4_pkt.src == h11.get_ip_addr() or ipv4_pkt.src == h12.get_ip_addr() or ipv4_pkt.src == h13.get_ip_addr():
                if ipv4_pkt.dst == h11.get_ip_addr() or ipv4_pkt.dst == h12.get_ip_addr() or ipv4_pkt.dst == h13.get_ip_addr():
                    out_port = u.host_to_port(subnet1, ipv4_pkt.dst)
                    actions = [parser.OFPActionOutput(out_port)]
                    self.permit_tcp(parser, ipv4_pkt,
                                    datapath, out_port)

        if udp_pkt and ipv4_pkt:

            # Attacker
            # Drop if destination is host h12
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h12.get_ip_addr():
                    actions = []
                    self.drop_udp(parser, ipv4_pkt, datapath)

            # Permit if destination is honeypot
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == honeypot.get_ip_addr():
                    actions = [parser.OFPActionOutput(
                        honeypot.get_gateway_port())]
                    self.permit_udp(parser, ipv4_pkt,
                                    datapath, honeypot.get_gateway_port())

            # Redirect to port 53 of honeypot if destination is host h13
            if ipv4_pkt.src == attacker.get_ip_addr():
                if ipv4_pkt.dst == h13.get_ip_addr():
                    if udp_pkt.dst_port == 123:
                        actions = [parser.OFPActionSetField(eth_dst=honeypot.get_MAC_addr()),
                                parser.OFPActionSetField(
                                    ipv4_dst=honeypot.get_ip_addr()),
                                parser.OFPActionSetField(udp_dst=123),
                                parser.OFPActionOutput(honeypot.get_gateway_port())]
                        self.redirect_udp(parser, ipv4_pkt, datapath, honeypot.get_gateway_port(), honeypot.get_MAC_addr(), honeypot.get_ip_addr(), udp_pkt.dst_port)
                  
                    
            # Honeypot
            # If response cames from honeypot to attacker(fagli credere che
            # la risposta proviene da h13)
            if ipv4_pkt.src == honeypot.get_ip_addr():
                if ipv4_pkt.dst == attacker.get_ip_addr():
                    actions = [parser.OFPActionSetField(eth_src=h13.get_MAC_addr()),
                               parser.OFPActionSetField(
                                   ipv4_src=h13.get_ip_addr()),
                               parser.OFPActionSetField(udp_src=123),
                               parser.OFPActionOutput(attacker.get_gateway_port())]
                    self.change_udp_src(parser, ipv4_pkt, datapath, attacker.get_gateway_port(
                    ), h13.get_MAC_addr(), h13.get_ip_addr())

            # Other hosts
            if ipv4_pkt.src == h11.get_ip_addr() or ipv4_pkt.src == h12.get_ip_addr() or ipv4_pkt.src == h13.get_ip_addr():
                if ipv4_pkt.dst == h11.get_ip_addr() or ipv4_pkt.dst == h12.get_ip_addr() or ipv4_pkt.dst == h13.get_ip_addr():
                    out_port = u.host_to_port(subnet1, ipv4_pkt.dst)
                    actions = [parser.OFPActionOutput(out_port)]
                    self.permit_udp(parser, ipv4_pkt,
                                    datapath, out_port)
        
        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=datap)
        datapath.send_msg(out)


# POLICIES
    # ARP


    def drop_arp(self, parser, arp_pkt, datapath, op_code):
        '''drop_arp'''
        actions = []
        match = parser.OFPMatch(
            eth_type=0x0806, arp_op=op_code, arp_spa=arp_pkt.src_ip, arp_tpa=arp_pkt.dst_ip)
        # self.logger.info(actions)
        # self.logger.info(match)
        self.add_flow(datapath, 101, match, actions)

    def permit_arp(self, parser, arp_pkt, datapath, op_code, out_port):
        '''permit_arp'''
        self.logger.info(out_port)
        actions = [parser.OFPActionOutput(out_port)]
        self.logger.info(actions)
        match = parser.OFPMatch(
            eth_type=0x0806, arp_op=op_code, arp_spa=arp_pkt.src_ip, arp_tpa=arp_pkt.dst_ip)
        self.add_flow(datapath, 101, match, actions)

    def redirect_arp(self, parser, arp_pkt, datapath, op_code, out_port, ip_honepot):
        '''redirect_arp'''
        actions = [parser.OFPActionSetField(arp_tpa=ip_honepot),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(
            eth_type=0x0806, arp_op=op_code, arp_spa=arp_pkt.src_ip, arp_tpa=arp_pkt.dst_ip)
        self.add_flow(datapath, 101, match, actions)

    # ICMP
    def drop_icmp(self, parser, ipv4_pkt, datapath, type_icmp):
        '''drop_icmp'''
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, icmpv4_type=type_icmp)
        self.add_flow(datapath, 102, match, actions)

    def redirect_icmp_echo_request(self, parser, ipv4_pkt, datapath, out_port,  mac_honeypot, ip_honeypot, type_icmp):
        '''redirect_icmp_echo_request'''
        actions = [parser.OFPActionSetField(eth_dst=mac_honeypot),
                   parser.OFPActionSetField(ipv4_dst=ip_honeypot),
                   parser.OFPActionOutput(out_port)]
        match = datapath.ofproto_parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_pkt.src, ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, icmpv4_type=type_icmp)
        self.add_flow(datapath, 102, match, actions)

    def change_icmp_src(self, parser, ipv4_pkt, datapath, out_port, mac_host, ip_host, type_icmp):
        '''change_icmp_src'''
        actions = [parser.OFPActionSetField(eth_src=mac_host),
                   parser.OFPActionSetField(ipv4_src=ip_host),
                   parser.OFPActionOutput(out_port)]
        match = datapath.ofproto_parser.OFPMatch(
            eth_type=0x800, ipv4_src=ipv4_pkt.src, ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, icmpv4_type=type_icmp)
        self.add_flow(datapath, 102, match, actions)

    def permit_icmp(self, parser, ipv4_pkt, datapath, out_port, type_icmp):
        '''permit_icmp'''
        actions = [parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, icmpv4_type=type_icmp)
        self.add_flow(datapath, 102, match, actions)

    # TCP

    def drop_tcp(self, parser, ipv4_pkt, datapath):
        '''drop_tcp'''
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto)
        self.add_flow(datapath, 103, match, actions)

    def permit_tcp(self, parser, ipv4_pkt, datapath, out_port):
        '''permit_tcp'''
        actions = [parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto)
        self.add_flow(datapath, 103, match, actions)

    def redirect_tcp(self, parser, ipv4_pkt, datapath, out_port, mac_honeypot, ip_honeypot, tcp_dst_port):
        '''redirect_tcp'''
        actions = [parser.OFPActionSetField(eth_dst=mac_honeypot),
                   parser.OFPActionSetField(ipv4_dst=ip_honeypot),
                   parser.OFPActionSetField(tcp_dst=tcp_dst_port),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, tcp_dst=tcp_dst_port)
        self.add_flow(datapath, 103, match, actions)

    def change_tcp_src(self, parser, ipv4_pkt, datapath, out_port, mac_host, ip_host, tcp_src_port):
        '''change_tcp_src'''
        actions = [parser.OFPActionSetField(eth_src=mac_host),
                   parser.OFPActionSetField(ipv4_src=ip_host),
                   parser.OFPActionSetField(tcp_src=tcp_src_port),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, tcp_src=tcp_src_port)
        self.add_flow(datapath, 103, match, actions)

    # UDP

    def drop_udp(self, parser, ipv4_pkt, datapath):
        '''drop_udp'''
        actions = []
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto)
        self.add_flow(datapath, 104, match, actions)

    def permit_udp(self, parser, ipv4_pkt, datapath, out_port):
        '''permit_udp'''
        actions = [parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto)
        self.add_flow(datapath, 104, match, actions)

    def redirect_udp(self, parser, ipv4_pkt, datapath, out_port, mac_honeypot, ip_honeypot, udp_dst_port):
        '''redirect_udp'''
        actions = [parser.OFPActionSetField(eth_dst=mac_honeypot),
                   parser.OFPActionSetField(ipv4_dst=ip_honeypot),
                   parser.OFPActionSetField(udp_dst=123),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto, udp_dst=udp_dst_port)
        self.add_flow(datapath, 104, match, actions)

    def change_udp_src(self, parser, ipv4_pkt, datapath, out_port, mac_host, ip_host):
        '''change_udp_src'''
        actions = [parser.OFPActionSetField(eth_src=mac_host),
                   parser.OFPActionSetField(ipv4_src=ip_host),
                   parser.OFPActionSetField(udp_src=123),
                   parser.OFPActionOutput(out_port)]
        match = parser.OFPMatch(eth_type=0x800, ipv4_src=ipv4_pkt.src,
                                ipv4_dst=ipv4_pkt.dst, ip_proto=ipv4_pkt.proto)
        self.add_flow(datapath, 104, match, actions)

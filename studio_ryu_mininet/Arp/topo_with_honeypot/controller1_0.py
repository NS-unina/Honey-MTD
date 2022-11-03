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
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
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

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # take arp packet.
        arp_pkt = pkt.get_protocol(arp.arp)
        if arp_pkt:
            if arp_pkt.opcode == arp.ARP_REQUEST and arp_pkt.src_ip == '10.0.1.10':
                if arp_pkt.dst_ip == '10.0.1.11': #or arp_pkt.dst_ip == '10.0.1.12':
                    #self.logger.info(arp_pkt)
                    actions = [parser.OFPActionOutput(ofproto.OFPC_FRAG_DROP)]
                    # vedi bene se la regola viene inserita
                    match = parser.OFPMatch(eth_type=0x800, arp_spa=arp_pkt.src_ip, arp_tpa=arp_pkt.dst_ip)
                    self.add_flow(datapath, 101, match, actions)

        # take icmp packet from insider attacker and redirects to honeypot.
        icmp_pkt = pkt.get_protocol(icmp.icmp)
        if icmp_pkt:
            self.logger.info(icmp_pkt)
            ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
            self.logger.info(ipv4_pkt)

            
            if ipv4_pkt.src == '10.0.1.10':
                #self.logger.info("Dpid %s", dpid)
                self.logger.info("src eth: %s", eth_pkt.src)
                self.logger.info("dst eth: %s", eth_pkt.dst)
                self.logger.info("dst ip: %s", ipv4_pkt.dst)
                out_port = 7
                actions = [parser.OFPActionSetField(eth_dst='00:00:00:00:00:09'),
                           parser.OFPActionSetField(ipv4_dst='10.0.1.200'),
                           parser.OFPActionOutput(out_port)]
                
                match = datapath.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_src='10.0.1.10')
                self.add_flow(datapath, 100, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=datap)
        datapath.send_msg(out)
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv6
from ryu.lib.packet import ipv4

class H1toH2(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *_args, **_kwargs):
        super(H1toH2, self).__init__(*_args, **_kwargs)
        self.mac_to_port = {}     #MAC address table


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]

        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS,
            actions
        )]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)


    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def __packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        dpid = datapath.id      #ID DELLO SWITCH
        self.mac_to_port.setdefault(dpid, {})


        #analizzare i pacchetti in ingresso -- focus on this
        #si prende protocollo, sorgente e destinazione
        #qui devo dire che se viene da una data sorgente allora lo devo mandare ad una data destinazione
        pkt = packet.Packet(msg.data)
        
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src


        
        ip4 = ''
        ip6 = ''
        out_port = ''
        #A quanto pare OpenFlow usa ipv6
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            ip4 = pkt.get_protocol(ipv4.ipv4)
            self.logger.info("ipv4_sorgente = %s", ip4.src)


        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            ip6 = pkt.get_protocol(ipv6.ipv6)
            self.logger.info("ipv6_sorgente = %s", ip6.src)

        

        in_port = msg.match['in_port']

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)


        #salvo nella mac table l'associazione sorgente-porta di ingresso
        self.mac_to_port[dpid][src] = in_port

        #devo agire nel momento in cui si scambiano i messaggi ARP 
        if ip4 == '10.0.0.1':
            out_port = 3
        elif dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        self.logger.info("OutPort = %s", out_port)
        actions = [parser.OFPActionOutput(out_port)]

        #per evitare di mandare i pacchetti in flooding nuovamente se la destinazione è nota
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=in_port, actions=actions, data=msg.data)

        datapath.send_msg(out)

        self.logger.info("-----------------------------------")


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
from ryu.lib.packet import arp

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
        ip4arp = ''
        out_port = ''
        
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            ip4 = pkt.get_protocol(ipv4.ipv4)
            self.logger.info("ipv4_sorgente = %s", ip4.src)


        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            ip6 = pkt.get_protocol(ipv6.ipv6)
            self.logger.info("ipv6_sorgente = %s", ip6.src)

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            ip4_arp = pkt.get_protocol(arp.arp)
            ip4arp = ip4_arp.src_ip
            self.logger.info("ipv6_arp = %s", ip4_arp)

        in_port = msg.match['in_port']

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)


        #salvo nella mac table l'associazione sorgente-porta di ingresso
        self.mac_to_port[dpid][src] = in_port

        #STEPS:
        #h1 ping h2
        #"10.0.0.1" manda in broadcast : "who has 10.0.0.2"
        #Il controller setta la out_port a 3 (porta dello switch che lo collega ocn 10.0.0.3)
        #Probabilmente 10.0.0.3 non risponde poichè non conosce il MAC di 10.0.0.2

        #Questa è la regola che si crea nella flow table dello switch
        #Vedi meglio i vari campi
        # cookie=0x0, duration=32.406s, table=0, n_packets=5, n_bytes=210, priority=1,
        # in_port="s1-eth1",dl_dst=ff:ff:ff:ff:ff:ff actions=output:"s1-eth3"
        if ip4arp == '10.0.0.1':
            out_port = 3
            actions = [parser.OFPActionOutput(out_port)
                #parser.OFPActionSetField(eth_dst='00:00:00:00:00:03')
            ]
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

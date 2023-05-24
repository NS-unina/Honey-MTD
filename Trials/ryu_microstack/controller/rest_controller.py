import json

import new_controller
from webob import Response
from  ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib import dpid as dpid_lib


name = 'rest_controller'
url = '/rest_controller/insert'

class RestController(new_controller.ExampleSwitch13):
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
    
    def drop(self, src_ip):
        '''drop'''
        datapath = self.switches.get(112935451091276)   #dpid - it 'll be passed from request
        parser = datapath.ofproto_parser
        actions = []
        match = parser.OFPMatch(
            eth_type=0x0800, ipv4_src=src_ip)
        # self.logger.info(actions)
        # self.logger.info(match)
        self.add_flow(datapath, 10001, match, actions)

class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[name]

    @route('restswitch', '/rest_controller/insert_rule', methods=['POST'])
    def insert_rule(self, req, **kwargs):
        richiesta = req.json
        simple_switch = self.simple_switch_app
        print(richiesta)
        if richiesta:
            actions = richiesta['actions']
            values = actions[0]
            t = values['type']
            match = richiesta['match']
            src = match['nw_src']
            if t == 'DROP':
                simple_switch.drop(src)
            return Response(status=200)
        else:
            return Response(status=400)

    
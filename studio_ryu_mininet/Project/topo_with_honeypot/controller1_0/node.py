class node(object):
    '''node object in a virtual topology'''
    def __init__(self, shortName=None, eth_addr=None, ip_addr=None, netmask=0, port=0, isHoneypot=False, 
                 isHost=False, isRouter=False, isServer=False, visible="nv"):
        self.shortName=shortName
        self.eth_addr=eth_addr
        self.ip_addr=ip_addr
        self.netmask=netmask
        self.port=port
        self.isHoneypot=isHoneypot      # vedi meglio come gestire la differenziazione tra i 
        self.isHost=isHost              # diversi tipi di nodo, così mi piace.
        self.isRouter=isRouter
        self.isServer=isServer
        self.visible=visible

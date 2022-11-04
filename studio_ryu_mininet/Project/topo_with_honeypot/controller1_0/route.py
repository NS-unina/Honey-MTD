class route(object):
    '''route object : collection of nodes of a virtual topology'''
    def __init__(self, startNode=None, endNode=None):
        self.startNode=startNode
        self.endNode=endNode
        self.hops=[]
        self.hops.append(startNode)
        self.hops.append(endNode)

    def add_hop(self, node):
        routeLen = len(self.hops)         # number of nodes in actual topology
        endNode = self.hops[routeLen - 1] # save endNode in a temp var
        self.hops[routeLen - 1] = node    # insert new node in route
        self.hops.append(endNode)         # replace end node

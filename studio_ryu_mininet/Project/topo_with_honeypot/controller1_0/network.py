from node import node
from subnet import subnet

# Da vedere meglio (capire come gestire la topologia virtuale)

class network(object):
    def __init__(self, subnets = list()):
        self.subnets = dict()
        for s in subnets:
            self.appendSub(s)
    
    def appendSub(self, subnet):
        keyS = str(subnet)
        self.subnets[keyS] = subnet

    def getSubnets(self):
        return self.subnets
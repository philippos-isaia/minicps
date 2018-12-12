"""
Scenario S1
Topology
"""

from mininet.topo import Topo
from utils import HOSTS, SWITCHES, CONNECTIONS, IP, MAC, NETMASKS
import logging

logging.basicConfig(format='PhyP::%(asctime)s::%(levelname)s::%(message)s', filename='master_log.log', level=logging.DEBUG)

print HOSTS
print len(HOSTS)
for host in HOSTS:
    print host
    print IP[host]
    print NETMASKS[host]
    print MAC[host]


'''
class MatlabTopo(Topo):

    def build(self):

        switch = self.addSwitch('s1')

        plc1 = self.addHost('plc1', ip=IP['plc1'] + NETMASK, mac=MAC['plc1'])

        self.addLink(plc1, switch)

        plc2 = self.addHost('plc2', ip=IP['plc2'] + NETMASK, mac=MAC['plc2'])

        self.addLink(plc2, switch)

'''
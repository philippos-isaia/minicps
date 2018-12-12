"""
Scenario S1
Topology
"""

from mininet.topo import Topo
from utils import HOSTS, SWITCHES, CONNECTIONS, IP, MAC, NETMASKS
import logging

logging.basicConfig(format='PhyP::%(asctime)s::%(levelname)s::%(message)s', filename='master_log.log', level=logging.DEBUG)

variables = {}


class MatlabTopo(Topo):

    def build(self):

        for switch in SWITCHES:
            variables[switch] = self.addSwitch(switch)

        for host in HOSTS:
            variables[host] = self.addHost(host, ip=IP[host]+NETMASKS[host], mac=MAC[host])

        for connection in CONNECTIONS:
            self.addLink(connection, CONNECTIONS[connection])

"""
Scenario S1
run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from mininet.node import OVSController
from topo import MatlabTopo
import sys


class MatlabS1(MiniCPS):

    """Creating main container for hosts and switches"""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc1, plc2, s1 = self.net.get('plc1', 'plc2', 's1')

        # Run PLC2 Code
        # plc1.cmd(sys.executable + ' plc1.py &')
        # Run PLC1 Code
        # plc2.cmd(sys.executable + ' plc2.py &')

        # Start Wireshark (tshark) on PLC1 capturing all interfaces
        plc1.cmd('touch plc1-eth0.pcap')
        plc1.cmd('chmod o=rw plc1-eth0.pcap')
        plc1.cmd('tshark -ni any -w plc1-eth0.pcap &')

        # Physical Process Might not be needed (check this out)
        # s1.cmd(sys.executable + ' physical_process.py &')

        CLI(self.net)

        net.stop()


if __name__ == "__main__":

    topo = MatlabTopo()
    net = Mininet(topo=topo, controller=OVSController)

    matlab_s1 = MatlabS1(
        name='matlab_s1',
        net=net)

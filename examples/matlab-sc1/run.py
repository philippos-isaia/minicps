"""
Scenario S1
run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from mininet.node import OVSController
from topo import MatlabTopo
from mininet.link import Intf
from utils import HOSTS, SWITCHES, NAT
from mininet.util import quietRun
from mininet.log import setLogLevel, info, error
import sys
import os
import time

os.system("sudo killall ovs-testcontroller")

def checkIntf( intf ):
    "Make sure intf exists and is not configured."
    config = quietRun( 'ifconfig %s 2>/dev/null' % intf, shell=True )
    if not config:
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', config )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
                               'and is probably in use!\n' )
        exit( 1 )


class MatlabS1(MiniCPS):

    """Creating main container for hosts and switches"""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()
        if NAT:
            print 'assigning IP addresses'
            for switch in SWITCHES:
                swi_for_edit = net.getNodeByName(switch)
                swi_for_edit.cmdPrint('dhclient '+swi_for_edit.defaultIntf().name)

            for host in HOSTS:
                ho_for_edit = net.getNodeByName(host)
                ho_for_edit.cmdPrint('dhclient '+ho_for_edit.defaultIntf().name)
                ho_for_edit.defaultIntf().updateIP()

            net.pingAll()
            for host in HOSTS:
                for_ip_print = net.getNodeByName(host)
                print str(host)+' IP: '+for_ip_print.IP()
            time.sleep(2)
            con = raw_input("Press enter to continue")


        # start devices
        plc1, plc2, coor = self.net.get('plc1', 'plc2', 'coor')

        # Run PLC2 Code
        # plc1.cmd(sys.executable + ' plc1.py &')
        # Run PLC1 Code
        # plc2.cmd(sys.executable + ' plc2.py &')

        # Start Wireshark (tshark) on PLC1 capturing all interfaces
        #plc1.cmd('touch plc1-eth0.pcap')
        #plc1.cmd('chmod o=rw plc1-eth0.pcap')
        #plc1.cmd('tshark -ni any -w plc1-eth0.pcap &')

        # This is the code that coordinator runs
        #coor.cmd(sys.executable + ' first_coordinator.py &')

        CLI(self.net)

        net.stop()


if __name__ == "__main__":

    topo = MatlabTopo()
    print 'creating topology'
    net = Mininet(topo=topo, controller=OVSController)
    if NAT:
        s1 = net.getNodeByName('s1')
        print 'adding interface eth1 to switch s1'
        Intf('eth1', node=s1)

    matlab_s1 = MatlabS1(name='matlab_s1', net=net)

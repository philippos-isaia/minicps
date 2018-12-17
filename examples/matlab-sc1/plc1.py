"""
Scenario S1
PLC1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import SEN_1, SEN_2, SEN_3, SEN_4, SEN_5
import logging
import time

logging.basicConfig(format='PLC1::%(asctime)s::%(levelname)s::%(message)s', filename='master_log.log', level=logging.DEBUG)
PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

s4 = ('s4', 1)
s5 = ('s5', 1)
# s6 = ('s6', 1)
serverIP = IP['plc1'] + ':502'

class MatlabPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        logging.debug('Enters pre_loop')
        time.sleep(2)

    def main_loop(self):
        """PLC1 main loop.

            - reads sensors s4 and s5 value
            - sends information to PLC2 so it can start the pump
        """

        logging.debug('Enters main_loop.')

        count = 0
        while(count <= PLC_SAMPLES):

            n04 = self.receive(SEN_4, serverIP)
            print 'Sensor S4 Value: '+str(n04)
            n05 = self.receive(SEN_5, serverIP)
            print 'Sensor S5 Value: '+str(n05)
            # Tank p1 fill percentage
            #tankp1 = float(self.get(s5))
            #flow_s4 = float(self.get(s4))
            # flow_s6 = float(self.get(s6))
            #logging.debug('Tank P1 fill level: %.5f' % tankp1)
            #self.send(s5, tankp1, PLC2_ADDR)
            #self.send(s4, flow_s4, PLC2_ADDR)
            # self.send(s6, flow_s6, PLC2_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1
        logging.debug('shutdown')


if __name__ == "__main__":

    plc1 = MatlabPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)

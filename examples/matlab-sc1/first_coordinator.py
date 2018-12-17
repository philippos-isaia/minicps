"""
Scenario S1
first_coordinator.py
Runs on switch s1 (coordinator)
Connection with Matlab
"""

from minicps.devices import Coordinator
from minicps.protocols import ModbusProtocol
from utils import S1_PROTOCOL
from utils import IP, STATE
from utils import PP_PERIOD_SEC
from utils import SEN_1, SEN_2, SEN_3, SEN_4, SEN_5
import sys
import logging
import time


S1_ADDR = IP['s1'] + ':502'
logging.basicConfig(format='PhyP::%(asctime)s::%(levelname)s::%(message)s', filename='logs/master_log.log', level=logging.DEBUG)

# sensors & actuators definition
sen_1 = ('s1', 1)
sen_2 = ('s2', 1)
sen_3 = ('s3', 1)
sen_4 = ('s4', 1)
sen_5 = ('s5', 1)
pump_2 = ('p2', 1)

serverIP = IP['s1'] + ':502'


class FirstCoordinator(Coordinator):

    def pre_loop(self):

        logging.debug('Enters pre_loop.')
        time.sleep(2)
        '''
        x = 121
        while True:
            self.send(('HR', 40), x, serverIP)
            x = x + 1
            time.sleep(1)
        '''

    def main_loop(self):

        logging.debug('Enters main_loop.')
        time.sleep(2)
        # Implement Saving Values to DB
        while True:
            '''
            n04 = self.receive(SEN_4, serverIP)
            self.send(('HR', 0), n04, '192.168.1.10:502')
            n05 = self.receive(SEN_5, serverIP)
            self.send(('HR', 8), n05, '192.168.1.10:502')
            
            n01 = self.receive(SEN_1, serverIP)
            print 'Sensor S1 Value: '+str(n01)
            n02 = self.receive(SEN_2, serverIP)
            print 'Sensor S2 Value: '+str(n02)
            n03 = self.receive(SEN_3, serverIP)
            print 'Sensor S3 Value: '+str(n03)
            n04 = self.receive(SEN_4, serverIP)
            print 'Sensor S4 Value: '+str(n04)
            n05 = self.receive(SEN_5, serverIP)
            print 'Sensor S5 Value: '+str(n05)
            '''
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    fcoo = FirstCoordinator(
        name='fcoo',
        protocol=S1_PROTOCOL,
        state=STATE
    )

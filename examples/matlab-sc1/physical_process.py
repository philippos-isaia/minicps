"""
Scenario S1
physical_process.py
Runs on switch s1 (coordinator)
Connection with Matlab
"""

from minicps.devices import Tank
from minicps.protocols import ModbusProtocol
from utils import S1_PROTOCOL, STATE
from utils import TANK_SECTION
from utils import RWT_INIT_LEVEL
from utils import IP
from utils import PP_PERIOD_SEC
from utils import SEN_1, SEN_2, SEN_3, SEN_4, SEN_5
import sys
import logging
import time
import struct

getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


def floatToBinary64(value):
    val = struct.unpack('Q', struct.pack('d', value))[0]
    return getBin(val)


def binaryToFloat(value):
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


S1_ADDR = IP['s1'] + ':502'
logging.basicConfig(format='PhyP::%(asctime)s::%(levelname)s::%(message)s', filename='logs/master_log.log', level=logging.DEBUG)

# sensors & actuators definition
sen_1 = ('s1', 1)
sen_2 = ('s2', 1)
sen_3 = ('s3', 1)
sen_4 = ('s4', 1)
sen_5 = ('s5', 1)
pump_2 = ('p2', 1)


class RawWaterTank(Tank):

    def pre_loop(self):

        logging.debug('Enters pre_loop.')
        self.set(pump_2, 0)
        self.level = self.set(sen_5, 0.800)
        #RTU2B_ADDR = IP['rtu2b'] + ':502'
        #HR_0_2a = ('HR', 0, '2a')
        #self.send(HR_0_2a, registers, '172.20.81.141:502', count=3)
        time.sleep(2)
        x = 121
        while True:
            self.send(('HR', 40), x, '172.20.81.141:502')
            x = x + 1
            time.sleep(1)

    def main_loop(self):

        logging.debug('Enters main_loop.')
        time.sleep(2)
        while True:
            '''
            n01 = self.receive(SEN_1, '172.20.81.141:502')
            print 'Sensor S1 Value: '+str(n01)
            n02 = self.receive(SEN_2, '172.20.81.141:502')
            print 'Sensor S2 Value: '+str(n02)
            n03 = self.receive(SEN_3, '172.20.81.141:502')
            print 'Sensor S3 Value: '+str(n03)
            n04 = self.receive(SEN_4, '172.20.81.141:502')
            print 'Sensor S4 Value: '+str(n04)
            n05 = self.receive(SEN_5, '172.20.81.141:502')
            print 'Sensor S5 Value: '+str(n05)
            '''
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        protocol=S1_PROTOCOL,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL,
        state=STATE
    )

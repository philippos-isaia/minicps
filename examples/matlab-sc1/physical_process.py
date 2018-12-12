"""
Scenario S1
physical_process.py
Runs on switch s1
Connection with Matlab
"""

from minicps.devices import Tank
from minicps.protocols import ModbusProtocol

from utils import S1_PROTOCOL
from utils import TANK_SECTION
from utils import RWT_INIT_LEVEL
from utils import STATE, IP, CO_0_2a
from utils import PP_PERIOD_SEC, PP_SAMPLES
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

# floats are represented by IEEE 754 floating-point format which are
# 64 bits long (not 32 bits)
S1_ADDR = IP['s1'] + ':502'
#S1_ADDR = 'localhost' + ':502'
logging.basicConfig(format='PhyP::%(asctime)s::%(levelname)s::%(message)s', filename='master_log.log', level=logging.DEBUG)

# sensors & pump definition
s1 = ('s1', 1)
s2 = ('s2', 1)
s3 = ('s3', 1)
s4 = ('s4', 1)
s5 = ('s5', 1)
p2 = ('p2', 1)
CO_0_2b = ('HR', 2, '2b')

class RawWaterTank(Tank):

    Swi1_TAGS = (
        ('s1', 1, 'REAL'),
        ('s2', 1, 'REAL'),
        ('s3', 1, 'REAL'),
        ('p2', 1, 'REAL'),
        ('s4', 1, 'REAL'),
        ('s5', 1, 'REAL'),
    )


    def pre_loop(self):

        logging.debug('Enters pre_loop.')
        self.set(p2, 0)
        self.level = self.set(s5, 0.800)


    def main_loop(self):

        logging.debug('Enters main_loop.')
        time.sleep(2)
        while True:
            CO_0_2a = ('CO', 0, '2a')
            n01 = self.receive(('HR', 0), '172.20.81.141:502')
            print 'Sensor S1 Value: '+str(n01)
            n02 = self.receive(('HR', 8), '172.20.81.141:502')
            print 'Sensor S2 Value: '+str(n02)
            n03 = self.receive(('HR', 16), '172.20.81.141:502')
            print 'Sensor S3 Value: '+str(n03)
            n04 = self.receive(('HR', 24), '172.20.81.141:502')
            print 'Sensor S4 Value: '+str(n04)
            n05 = self.receive(('HR', 32), '172.20.81.141:502')
            print 'Sensor S5 Value: '+str(n05)
            #+','+str(n02)+','+str(n03)+','+str(n04)+','+str(n05)+','+str(n06)+','+str(n07)
            #tttt=floatToBinary64(float(n01))
            #print 'float to binary: ' + str(floatToBinary64(tttt))
            #print 'binary to float: ' + str(binaryToFloat(tttt))
            # self.send(('CO', 0, '2a'), False, '172.20.81.141:502')
            # new_level = self.receive(('CO', 0, '2a'), '172.20.81.141:502')
            '''
            try:
                new_level = self.receive(('HR', 2), 502)
                print (new_level)
            except:
                print 'problem'
            '''
            # compute water volume
            # water_volume = self.section * new_level
            # test = self.receive(('CO', 62), '172.20.81.141:5020')
            # print test
            # logging.debug('Received from 172:...:38: '+test)
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=S1_PROTOCOL,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )

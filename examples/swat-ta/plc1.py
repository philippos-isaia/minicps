"""
swat-ta plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP
from utils import T_LIT101_M, T_LIT301_M, T_FIT201
from utils import LIT101_1, MV101_1, P101_1

import time


class SwatPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-ta plc1 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-ta plc1 enters main_loop.'
        print

        while(True):

            # NOTE: lit101 [meters]
            lit101 = float(self.get(LIT101))
            print 'DEBUG plc1 lit101: %.5f' % lit101
            self.send(LIT101_1, lit101, IP['plc1'])

            # NOTE: blocking read fit201 and lit301 interlocks
            fit201 = float(self.receive(FIT201_2, IP['plc2']))
            print "DEBUG PLC1 - receive fit201: %f" % fit201
            self.send(FIT201_1, fit201, IP['plc1'])
            lit301 = float(self.receive(LIT301_3, IP['plc3']))
            print "DEBUG PLC1 - receive lit301: %f" % lit301
            self.send(LIT301_1, lit301, IP['plc1'])

            if lit101 <= T_LIT101_M['L']:
                # NOTE: close mv101
                self.set(MV101_1, 1)
                self.memory['MV101_1'] = 1
            if lit101 >= T_LIT101_M['H']:
                # NOTE: close mv101
                self.set(MV101_1, 0)
                self.memory['MV101_1'] = 0
            if lit101 <= T_LIT101_M['LL']:
                # NOTE: stop p101
                self.set(P101_1, 0)
                self.memory['P101_1'] = 0
                # TODO: add alarm to state
                print('ALARM: lit101 below LL: {}'.format(lit101))
            if lit101 >= T_LIT101_M['HH']:
                print('ALARM: lit101 above HH: {}'.format(lit101))

            # FIXME: no check about lit301 integrity
            if lit301 <= T_LIT301_M['L']:
                # NOTE: start p101
                self.set(P101_1, 1)
                self.memory['P101_1'] = 1
            if lit301 >= T_LIT301_M['H'] or fit201 <= T_FIT201:
                # NOTE: stop p101
                self.set(P101_1, 0)
                self.memory['P101_1'] = 0

            # NOTE: update internal enip server
            self.send(MV101_1, self.memory['MV101_1'], IP['plc1'])
            self.send(P101_1, self.memory['P101_1'], IP['plc1'])

            time.sleep(PLC_PERIOD_SEC)

        print 'DEBUG swat-ta plc1 shutdown'


if __name__ == "__main__":

    plc1 = SwatPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
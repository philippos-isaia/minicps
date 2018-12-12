"""
Scenario S1
PLC2.py
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP
from utils import tankp1_M

import logging
import time

logging.basicConfig(format='PLC2::%(asctime)s::%(levelname)s::%(message)s', filename='master_log.log', level=logging.DEBUG)

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

s1 = ('s1', 1)
s2 = ('s2', 1)
s3 = ('s3', 1)
s4 = ('s4', 1)
s5 = ('s5', 1)
#s6 = ('s6', 2)
p2 = ('p2', 1)


class MatlabPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        logging.debug('Enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """PLC2 main loop.
            - read sensors s1, s2, s3
            - act on pump p2
            - update internal enip server
        """

        logging.debug('Enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):

            pres_s1 = float(self.get(s1))
            logging.debug("Pressure at s1: %f" % pres_s1)
            pres_s2 = float(self.get(s2))
            logging.debug("Pressure at s2: %f" % pres_s2)
            flow_s3 = float(self.get(s3))
            logging.debug("Flow at s3: %f" % flow_s3)
            pump_p2 = float(self.get(p2))
            logging.debug("Pump state at: %f" % pump_p2)

            # flow_s4 = float(self.receive(s4, PLC1_ADDR))
            # flow_s6 = float(self.receive(s6, PLC1_ADDR))
            tankp1 = float(self.receive(s5, PLC1_ADDR))

            if tankp1 >= tankp1_M['HH']:
                logging.warning("Tank P1 over HH: %.2f >= %.2f." % (tankp1, tankp1_M['HH']))

            if tankp1 >= tankp1_M['H']:
                # Stop Pump p2
                logging.info("Tank P1 over H -> stop Pump P2.")
                self.set(p2, 0)
                self.send(p2, 0, PLC1_ADDR)

            elif tankp1 <= tankp1_M['LL']:
                logging.warning("Tank P1 under LL: %.2f <= %.2f." % (tankp1, tankp1_M['LL']))
                logging.info("Start Pump P2.")
                self.set(p2, 1)
                self.send(p2, 1, PLC1_ADDR)

            elif tankp1 <= tankp1_M['L']:
                # Start Pump p2
                logging.info("Tank P1 L -> start Pump P2.")
                self.set(p2, 1)
                self.send(p2, 1, PLC1_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        logging.debug('Shutdown')


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = MatlabPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)

"""
Scenario S1
Connection with Matlab
"""

from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

# Define physical constants that can be used
# by the Coordinator & PLCs for
# decision making

GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 2.55        # m^3/h
PUMP_FLOWRATE_OUT = 2.45       # m^3/h

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 1.00

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Define control logic thresholds
tankp1_M = {
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 0.900,
}

# IP, Netmask and MAC addresses

# Here you define the topology
# use the HOSTS list to define the names of the hosts
# this includes PLCs, attackers or any other host but NOT the coordinator or switches

HOSTS = ['coor', 'plc1', 'plc2', 'attacker']

# use the SWITCHES list to define the names of the coordinators or switches

SWITCHES = ['s1']

NAT = True
# use the IP dictionary to define the IP addresses of each component
# i.e. hosts and switches

IP = {
    'coor': '192.168.1.10',
    'plc1': '192.168.1.20',
    'plc2': '192.168.1.30',
    'attacker': '192.168.1.50',
    's1': '172.20.81.141',
}

NETMASK = '/24'

# use the NETMASKS dictionary to define the netmasks

NETMASKS = {
    'coor': '/24',
    'plc1': '/24',
    'plc2': '/24',
    'attacker': '/24',
    's1': '/24',
}

# use the MAC dictionary to define the MAC addresses of each component
# i.e. hosts and switches

MAC = {
    'coor': '00:1D:9C:C7:B0:30',
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'attacker': '00:1D:9C:C8:BC:48',
    's1': '08:00:27:39:a6:83',
}

# use the CONNECTIONS dictionary to define the connections between
# hosts and switches
# note: connections are bidirectional, therefore define them once

CONNECTIONS = {
    'coor': 's1',
    'plc1': 's1',
    'plc2': 's1',
    'attacker': 's1',
}

# global definitions for sensors and actuators

sen_1 = ('s1', 1, 'REAL')
sen_2 = ('s2', 1, 'REAL')
sen_3 = ('s3', 1, 'REAL')
sen_4 = ('s4', 1, 'REAL')
sen_5 = ('s5', 1, 'REAL')
pump_1 = ('p2', 1, 'REAL')


# definitions for reading modbus/enip messages
# for modbus use:
# CO (1-bit, coil, read and write)
# DI (1-bit, discrete input, read only)
# HR (16-bit, holding register, read and write)
# IR (16-bit, input register, read only)
# plus the offset

SEN_1 = ('HR', 0)
SEN_2 = ('HR', 8)
SEN_3 = ('HR', 16)
SEN_4 = ('HR', 24)
SEN_5 = ('HR', 32)

# PLC1 Data
PLC1_ADDR = IP['plc1']
#PLC1_TAGS = (sen_4, sen_5,)
PLC1_TAGS = (10, 10, 10, 100)
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS
}
PLC1_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': PLC1_SERVER
}

# PLC2 Data
PLC2_ADDR = IP['plc2']
PLC2_TAGS = (sen_1, sen_2, sen_3, sen_4, sen_5, pump_1,)
'''
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': PLC2_SERVER
}
'''
COOR_TAGS = (10, 10, 10, 100)
COOR_ADDR = IP['coor']
COOR_SERVER = {
    'address': COOR_ADDR,
    'tags': COOR_TAGS
}
COOR_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': COOR_SERVER
}
'''
COORDINATOR_TAGS = (10, 10, 10, 100)
COORDINATOR_ADDR = IP['coor']
COORDINATOR_SERVER = {
    'address': COORDINATOR_ADDR,
    'tags': COORDINATOR_TAGS
}
COORDINATOR_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': COORDINATOR_SERVER
}
'''
# TODO
PLC1_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC2_DATA = {
    'TODO': 'TODO',
}

PATH = 'matlab_sc1_db.sqlite'
NAME = 'matlab_sc1'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE matlab_sc1 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO matlab_sc1 VALUES ('s1', 1, '0.0');
    INSERT INTO matlab_sc1 VALUES ('s2', 1, '0.0');
    INSERT INTO matlab_sc1 VALUES ('s3', 1, '0.0');
    INSERT INTO matlab_sc1 VALUES ('s4', 1, '0.0');
    INSERT INTO matlab_sc1 VALUES ('s5', 1, '0.0');
    INSERT INTO matlab_sc1 VALUES ('p2', 1, '100');
"""
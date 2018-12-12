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

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 2.55        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 2.45       # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
tankp1_M = {  # raw water tank m
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 0.900,
}

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

# IP, Netmask and MAC addresses

CO_0_2a = ('HR', 0, '2a')
IP = {
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    's1': '172.20.81.141',
}

NETMASK = '/24'

MAC = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    's1': '08:00:27:39:a6:83',
}

# PLC1 Data
PLC1_ADDR = IP['plc1']
PLC1_TAGS = (
    ('s4', 1, 'REAL'),
    ('s5', 1, 'REAL'),
)
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS
}
PLC1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC1_SERVER
}

# PLC2 Data
PLC2_ADDR = IP['plc2']
PLC2_TAGS = (
    ('s1', 1, 'REAL'),
    ('s2', 1, 'REAL'),
    ('s3', 1, 'REAL'),
    ('p2', 1, 'REAL'),
    ('s4', 1, 'REAL'),
    ('s5', 1, 'REAL'),
)

PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC2_SERVER
}
S1_TAGS = (10, 10, 10, 100)
S1_ADDR = IP['s1']
S1_SERVER = {
    'address': S1_ADDR,
    'tags': S1_TAGS
}
S1_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': S1_SERVER
}

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
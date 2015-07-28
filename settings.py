from enum import IntEnum
from EdisonPort import EdisonPort
from DebugPort import DebugPort

### COMMON
# networking
PORT = 3456

### CLIENT
INPUT_PORT = 'KeyLab 49 MIDI 1'
SERVER_ADDRESS = '192.168.1.136'

### SERVER
PORT_TYPE = DebugPort
LISTEN_ADDRESS = '0.0.0.0'
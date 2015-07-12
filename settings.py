from enum import IntEnum
from EdisonPort import EdisonPort
from DebugPort import DebugPort

### COMMON
# networking
PORT = 3456
# messages (command (1), timing (3), data[] (4))
MSG_LENGTH = 8  # should be a power of 2
class MAPPINGS(IntEnum):
    RESET = 0
    NOTE_ON = 1  # key, velo
    NOTE_OFF = 2 # key
    SUS_ON = 3
    SUS_OFF = 4

### CLIENT
INPUT_PORT = 'Midi Through Port-0'

### SERVER
PORT_TYPE = DebugPort
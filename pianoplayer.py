import mido
import time
from edi_port import EdiPort

midi_file = mido.MidiFile('./clairedelune.mid')
port = EdiPort()

# play song
for msg in midi_file:
    time.sleep(msg.time)
    if not isinstance(msg, mido.MetaMessage):
        port.send(msg)
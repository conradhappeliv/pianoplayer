import time
import mido


def play_file(filen, port, stopevent):
    # piano takes 2 seconds to warm up
    port.write([0x90, 0xFF, 0x00])
    time.sleep(2)

    midi_file = mido.MidiFile('files/'+filen)
    for msg in midi_file:
        if stopevent.is_set():
            return 0
        time.sleep(msg.time)
        if not isinstance(msg, mido.MetaMessage):
            port.send(msg)
    return 0
from mido.ports import BaseIOPort

class DebugPort(BaseIOPort):
    def _open(self, **kwargs):
        print("MIDI port connected")

    def _close(self):
        print("MIDI port disconnected")

    def _send(self, message):
        print(message)

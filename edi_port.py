import serial
from mido.ports import BaseIOPort


class EdiPort(BaseIOPort):
    def _open(self, **kwargs):
        self.port = serial.Serial('/dev/ttyMFD1', 31250)  # https://communities.intel.com/thread/54236

    def _close(self):
        self.port.close()

    def _send(self, message):
        self.port.write(message.bytes())
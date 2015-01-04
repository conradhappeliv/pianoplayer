import serial
from mido.ports import BaseIOPort


class EdiPort(BaseIOPort):
    def _open(self, **kwargs):
        try:
            self.port = serial.Serial('/dev/ttyMFD1', 31250)  # https://communities.intel.com/thread/54236
            self.connected = True
        except serial.SerialException:
            print "Unable to connect to serial port. Running in test mode."
            self.connected = False

    def _close(self):
        if self.connected:
            self.port.close()

    def _send(self, message):
        if self.connected:
            self.port.write(message.bytes())
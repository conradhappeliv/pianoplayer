import zmq
import settings
import threading
import queue
import time
import mido

from translators import decode_command

q = queue.Queue()

def server():
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)
    zmq_socket.bind('tcp://127.0.0.1:'+str(settings.PORT))

    while True:
        q.put(zmq_socket.recv())
        zmq_socket.send_string('ack')  # pattern requires reply

def player():
    last_played_at = time.time()
    port = settings.PORT_TYPE()

    while True:
        cur = q.get()  # blocks until something in queue
        decoded = decode_command(cur)
        diff = last_played_at + decoded['timing']/1000 - time.time()
        # TODO: add "wake-up" for piano
        if diff > 0:
            time.sleep(diff)
        if decoded['command'] == settings.MAPPINGS.RESET:
            msg = mido.Message('reset')
        elif decoded['command'] == settings.MAPPINGS.NOTE_ON:
            msg = mido.Message('note_on', note=decoded['data'][0], velocity=decoded['data'][1])
        elif decoded['command'] == settings.MAPPINGS.NOTE_OFF:
            msg = mido.Message('note_off', note=decoded['data'][0])
        elif decoded['command'] == settings.MAPPINGS.SUS_ON:
            msg = mido.Message('control')  # TODO
        elif decoded['command'] == settings.MAPPINGS.SUS_OFF:
            msg = mido.Message('control')  # TODO
        port.send(msg)
        last_played_at = time.time()

def main():
    threading.Thread(target=server).start()
    threading.Thread(target=player).start()

if __name__ == '__main__':
    main()

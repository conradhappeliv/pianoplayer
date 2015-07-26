import zmq
import settings
import threading
import queue
import time
import mido

q = queue.Queue()


def server():
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)
    zmq_socket.bind('tcp://0.0.0.0:'+str(settings.PORT))

    while True:
        q.put((zmq_socket.recv(), time.time()))
        zmq_socket.send_string('ack')  # pattern requires reply


def player():
    last_played_at = time.time()
    port = settings.PORT_TYPE()

    while True:
        cur, recv_time = q.get()  # blocks until something in queue
        timing = int.from_bytes(cur[0:4], 'big')

        while time.time() - recv_time < 5: pass # 5 second "buffer" time

        diff = last_played_at + timing/1000 - time.time()

        if time.time() - last_played_at > 30: # piano wakeup
            port.send(mido.Message('reset'))
            time.sleep(2.5)

        if diff > 0:  # timing between notes
            time.sleep(diff)

        message = mido.parse(cur[4:])

        port.send(message)
        last_played_at = time.time()

def main():
    threading.Thread(target=server).start()
    threading.Thread(target=player).start()

if __name__ == '__main__':
    main()

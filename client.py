import zmq
import settings
import queue
import threading
import curses
import time
import mido

last_time = time.time()
stdscr = curses.initscr()
stdscr.keypad(1)
stdscr.refresh()

q = queue.Queue()


def player():
    global last_time
    while True:
        key = stdscr.getch()
        now_time = time.time()
        timing = now_time - last_time
        timing = int(timing*1000)
        q.put((chr(key), timing))
        last_time = now_time


def sender():
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REQ)
    zmq_socket.connect('tcp://127.0.0.1:'+str(settings.PORT))
    while True:
        letter, timing = q.get()
        if letter == 'a':
            note = 60
        elif letter == 's':
            note = 62
        elif letter == 'd':
            note = 64
        elif letter == 'f':
            note = 65
        elif letter == 'g':
            note = 67
        message = mido.Message('note_on', note=note, velocity=90)
        message_bytes = timing.to_bytes(4, 'big')  # allow 4 bytes for timing (up to 4294967.296 seconds)
        message_bytes += message.bin()
        zmq_socket.send(message_bytes)
        zmq_socket.recv_string()


def main():
    threading.Thread(target=player).start()
    threading.Thread(target=sender).start()

if __name__ == '__main__':
    main()
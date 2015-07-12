import zmq
import settings
import mido

from translators import generate_command

zmq_context = zmq.Context()

def main():
    zmq_socket = zmq_context.socket(zmq.REQ)
    zmq_socket.connect('tcp://127.0.0.1:'+str(settings.PORT))

    inport = mido.open_input(settings.INPUT_PORT)

    for msg in inport:
        print(msg)
        # sustain is control 64
        comm = generate_command(msg.type, 1000, msg.note, msg.velocity)
        zmq_socket.send(comm)
        zmq_socket.recv_string()  # ack'd


if __name__ == '__main__':
    main()
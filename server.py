import settings
import threading
import queue
import time
import mido
import os
import tornado.ioloop
import tornado.web
import tornado.websocket

q = queue.Queue()
connected = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        connected.append(self)

    def close(self, code=None, reason=None):
        pass

    def on_message(self, message):
        message = message.split(',')
        timing = int(message[0])
        midi_cmd = mido.parse(bytearray([int(x) for x in message[1:]]))
        q.put((midi_cmd, timing, time.time()))


def player():
    last_played_at = time.time()
    port = settings.PORT_TYPE()

    while True:
        message, timing, recv_time = q.get()  # blocks until something in queue

        while time.time() - recv_time < 5: pass # 5 second "buffer" time

        diff = last_played_at + timing/1000 - time.time()

        if time.time() - last_played_at > 30: # piano wakeup
            port.send(mido.Message('reset'))
            time.sleep(2.5)

        if diff > 0:  # timing between notes
            time.sleep(diff)

        port.send(message)
        last_played_at = time.time()

def server():
    tornado_settings = {
        'debug': True,
        'static_path': os.path.dirname(os.path.realpath(__file__))+'/static',
        'template_path': os.path.dirname(os.path.realpath(__file__))+'/static'
    }
    urls = [
        (r'/', MainHandler),
        (r'/ws', WSHandler)
    ]
    app = tornado.web.Application(urls, **tornado_settings)
    app.listen(settings.PORT)
    tornado.ioloop.IOLoop.current().start()

def main():
    threading.Thread(target=player).start()
    server()

if __name__ == '__main__':
    main()

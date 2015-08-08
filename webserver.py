import settings
import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado import gen
from threading import Timer

player_queue = []
piano_connection = None

class IncomingWSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        player_queue.append(self)
        self.send_position()

    def on_close(self):
        player_queue.remove(self)
        for player in player_queue:
            player.send_position()

    def on_message(self, message):
        if player_queue[0] is not self:
            return
        else:
            if not self.timer:
                self.timer = Timer(settings.PLAY_TIME, self.close)
            piano_connection.write_message(message)

    def send_position(self):
        self.write_message({"position": player_queue.index(self)+1})


def server():
    urls = [
        (r'/', IncomingWSHandler)
    ]
    app = tornado.web.Application(urls)
    app.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()

@gen.coroutine
def connect_to_piano():
    global piano_connection
    piano_connection = yield tornado.websocket.websocket_connect('ws://'+settings.PIANO_ADDRESS+':'+str(settings.PORT)+'/ws')


def main():
    connect_to_piano()
    server()


if __name__ == '__main__':
    main()

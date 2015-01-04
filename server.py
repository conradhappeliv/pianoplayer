import cherrypy
import os
import multiprocessing
import playerworker
from edi_port import EdiPort
port = EdiPort()


class PianoPlayer(object):
    def __init__(self):
        self.player = multiprocessing.Process()
        self.stopevent = multiprocessing.Event()

    @cherrypy.expose
    def index(self):
        return file('static/index.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getlist(self):
        if not os.path.exists('files'):
            os.mkdir('files')
            return {}
        else:
            return os.listdir('files')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def start(self, filename='clairdelune.mid'):
        if self.player.is_alive():
            print "Already playing"
            return 1
        else:
            self.player = multiprocessing.Process(target=playerworker.play_file, args=(filename, port, self.stopevent))
            self.player.start()
            print "Playing started"
            return 0

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        if self.player.is_alive():
            self.stopevent.set()
            self.player.join()
            self.stopevent.clear()
            print "Playing stopped"
            return 0
        else:
            print "Not playing, can't stop"
            return 1

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.dirname(os.path.realpath(__file__))
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    cherrypy.quickstart(PianoPlayer(), '/', conf)
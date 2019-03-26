import json

import zmq
from zmq.eventloop import ioloop, zmqstream

ioloop.install()


class Broker(object):

    def __init__(self):
        self._publisher = None
        self._suscriber = None
        self._pairs = []

    def setPublisher(self, port):
        self._publisher = Publisher(port)

    def publish(self, topic, message):
        self._publisher.send(topic, message)

    def setSuscriber(self, ip, port):
        self._suscriber = Suscriber(ip, port)
        self._suscriber.connect()

    def suscribe(self, topics, callback):
        self._suscriber.suscribe(topics, callback)

    def listen(self):
        """
        Starts polling the suscribed/ peer sockets already connected to
        Blocks the process/ thread that called it
        """
        ioloop.IOLoop.current(instance=True).start()

    def peek(self, topics):
        return self._suscriber.peek(topics)

    def addPeer(self, ip, port):
        pass


class Publisher(object):

    def __init__(self, port):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%d" % (self.port))
        print("ZeroMQ Publisher bound on tcp://*:%d" % self.port)

    def send(self, topic, message):
        # message['type'] = message
        # self.socket.send_json(message)
        json_string = json.dumps(message)
        self.socket.send("%s %s" % (topic, json_string))


class Suscriber(object):

    def __init__(self, ip, port, topics):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.port = port
        self.ip = ip
        self._stream_sub = None
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

    def connect(self):
        print("Connecting Suscriber to tcp://%s:%d" % (self.ip, self.port))
        errok = self.socket.connect("tcp://%s:%d" % (self.ip, self.port))
        if (errok):
            print("Connection returned error: ")
            print(errok)

    def suscribe(self, callback):
        """
        add a callback for this subscriber
        """
        self._stream_sub = zmqstream.ZMQStream(self.socket)
        self._stream_sub.on_recv(callback)

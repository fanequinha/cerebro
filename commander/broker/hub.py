import zmq
import socket
import sys
import json
import time
import base64

# ------------------------------
class Publisher(object):

    def __init__(self, port):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%d" % (self.port))
        print ("ZeroMQ bound on tcp://*:%d" % (self.port))

    def send(self, topic, message):
        
        json_string = base64.b64encode(json.dumps(message))
        self.socket.send("%s %s" % (topic, json_string))

# ------------------------------
class Suscriber(object):

    def __init__(self, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.port = port
        self.ip = ip
        

    def connect(self):
            print("Connecting Suscriber to tcp://%s:%d" % (self.ip, self.port))
            errok = self.socket.connect("tcp://%s:%d" % (self.ip, self.port))
            print("Connection returned: ")
            print(errok)

    def listen(self, topic):
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        while True:
            rcvd = self.socket.recv()
            topic, msg = rcvd.split()
            msg = base64.b64decode(msg)
            if (topic == "TLM"):
                print ("Received message: " + msg)
            else:
                print ("Unknown topic")
            if (msg == "q"):
                sys.exit()
            time.sleep(1)


def main():
    bksrv = Suscriber("localhost", 5555)
    bksrv.connect()
    bksrv.listen("TLM")

if __name__ == "__main__":
    import sys

    main()
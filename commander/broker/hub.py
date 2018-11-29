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
        time.sleep(2)

    # --------
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
        

    # --------
    def connect(self):
            print("Connecting Suscriber to tcp://%s:%d" % (self.ip, self.port))
            errok = self.socket.connect("tcp://%s:%d" % (self.ip, self.port))
            print("Connection returned: ")
            print(errok)

    # --------
    def listen(self, topics):
        """
        Blocks and waits for a message of any of the topics in the array
        returns the topic and message as a named tuple
        There can be more messages still in the queue
        """
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        
        rcvd = self.socket.recv()
        topic, msg = rcvd.split()
        msg = base64.b64decode(msg)
        
        print ("[%s] Received message: %s" % (topic, msg))

        return (topic, json.loads(msg))

    # --------
    def peek(self, topics):
        """
        Tries to receive message of any of the topics in the array
        does not block; returns the topic and message as a named tuple, or
        if there were no messages, returns topic "BOO"
        """
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        try:
            rcvd = self.socket.recv(flags=zmq.NOBLOCK)
            topic, msg = rcvd.split()
            msg = base64.b64decode(msg)

            return (topic, json.loads(msg))

        except zmq.ZMQError as e:
            topic = 'BOO'
            return ('BOO', None)


# ------------------------------

def main():
    bksrv = Suscriber("localhost", 5555)
    bksrv.connect()
    topic = ''
    count = 0
    while True:
        while topic != 'BOO':
            topic, message = bksrv.peek(["POS", "STS", "DBG"])
            if (topic != 'BOO'):
                print("Received [%d][%s] message:" % (count,topic))
                print (json.dumps(message, indent=4, sort_keys=True))
                count += 1
            sys.stdout.write("#")
            sys.stdout.flush()
        topic = ''
        time.sleep(.1)


if __name__ == "__main__":
    import sys

    main()
from socket import socket
import traceback
from threading import Thread
import struct


class VirtualPushBotRetina(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.setDaemon(True)
        self._socket = socket
        self._started = False

    def run(self):
        self._started = True
        polarity = 0
        connected = True
        while connected and self._started:
            try:
                for x in range(128):
                    for y in range(128):
                        value = 0x8000 | y << 8 | polarity << 7 | x
                        data = struct.pack("<H", value)
                        self._socket.send(data)
                polarity = (polarity + 1) % 1
            except:
                traceback.print_exc()
                connected = False
                self._started = False
        print "Retina stopped"

    def stop(self):
        self._started = False


sock = socket()
sock.bind(("0.0.0.0", 56000))
sock.listen(1)
retina = None

while True:
    print "Waiting for connection"
    connection, client = sock.accept()
    print "Client Connected from {}".format(client)

    is_data = True
    while is_data:
        data = None
        try:
            data = connection.recv(200)

            if not data:
                is_data = False
            else:
                print "RECV: {}".format(data)
                if data == "E+\n":
                    print "Starting retina"
                    retina = VirtualPushBotRetina(connection)
                    retina.start()
                elif data == "E-\n" and retina is not None:
                    print "Stopping retina"
                    retina.stop()
                    retina = None
        except:
            traceback.print_exc()
            is_data = False

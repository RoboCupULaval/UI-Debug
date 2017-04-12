# Under MIT License, see LICENSE.txt

__author__ = 'RoboCupULaval'

from socketserver import ThreadingMixIn, UDPServer, BaseRequestHandler
import threading
import socket
import struct


def getUDPHandler(receiver):
    class ThreadedUDPRequestHandler(BaseRequestHandler):
        def handle(self):
            data = self.request[0]
            receiver.set_current_frame(data)

    return ThreadedUDPRequestHandler


class ThreadedUDPServer(ThreadingMixIn, UDPServer):
    allow_reuse_address = True

    def __init__(self, host, port, receiver):
        handler = getUDPHandler(receiver)
        super(ThreadedUDPServer, self).__init__(('', port), handler)
        self.socket.setsockopt(socket.IPPROTO_IP,
                               socket.IP_ADD_MEMBERSHIP,
                               struct.pack("=4sl",
                                           socket.inet_aton(host),
                                           socket.INADDR_ANY))
        server_thread = threading.Thread(target=self.serve_forever)
        server_thread.daemon = True
        server_thread.start()


class PBPacketReceiver(object):
    def __init__(self, host, port, packet_type):
        self.current_packet = None
        self.lock = threading.Lock()
        self.packet_type = packet_type
        self.server = ThreadedUDPServer(host, port, self)

    def set_current_frame(self, data):
        self.lock.acquire()
        self.current_data = data
        self.lock.release()

    def get_latest_frame(self):
        if self.current_data is None:
            return None
        packet = self.packet_type()
        self.lock.acquire()
        packet.ParseFromString(self.current_data)
        self.lock.release()
        return packet

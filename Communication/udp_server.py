# Under MIT License, see LICENSE.txt

__author__ = 'RoboCupULaval'

from socketserver import ThreadingMixIn, UDPServer, BaseRequestHandler
import threading
import socket
import struct


def getUDPHandler(receiver):
    class ThreadedUDPRequestHandler(BaseRequestHandler):
        def handle(self):
            frame = self.request[0]
            receiver.add_frame(frame)

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
        self.received_frames = []
        self.lock = threading.Lock()
        self.packet_type = packet_type
        self.server = ThreadedUDPServer(host, port, self)

    def add_frame(self, frame):
        self.lock.acquire()
        self.received_frames.append(frame)
        self.lock.release()

    def get_latest_frames(self):
        if len(self.received_frames) == 0:
            return []

        self.lock.acquire()
        frames = self.received_frames.copy()
        self.received_frames.clear()
        self.lock.release()

        packets = []
        for frame in frames:
            packet = self.packet_type()
            packet.ParseFromString(frame)
            packets.append(packet)
        return packets

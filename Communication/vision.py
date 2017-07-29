# Under MIT License, see LICENSE.txt

from Communication import messages_robocup_ssl_wrapper_pb2 as ssl_wrapper
from Communication.udp_server import PBPacketReceiver

__author__ = 'RoboCupULaval'


class Vision(PBPacketReceiver):
    def __init__(self, host="224.5.23.2", port=10024):
        self._default_ip = "224.5.23.2"
        self._default_port = 10024
        self._ip = host
        self._port = port
        super().__init__(host, port, ssl_wrapper.SSL_WrapperPacket)

    def get_ip(self):
        return self._ip

    def get_default_ip(self):
        return self._default_ip

    def get_default_port(self):
        return self._default_port

    def get_port(self):
        return self._port

    def set_new_connexion(self, ip, port):
        self._ip = ip
        self._port = port
        super().__init__(ip, port, ssl_wrapper.SSL_WrapperPacket)

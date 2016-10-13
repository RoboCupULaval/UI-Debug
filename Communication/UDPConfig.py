# Under MIT License, see LICENSE.txt

__author__ = 'RoboCupULaval'


class UDPConfig():
    def __init__(self, host="224.5.23.2", port=10020):
        self._default_ip = "224.5.23.2"
        self._default_port = 10020
        self._ip = host
        self._port = port

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    def get_default_ip(self):
        return self._default_ip

    def get_default_port(self):
        return self._default_port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
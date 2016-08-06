# Under MIT License, see LICENSE.txt

import logging
import pickle
import socket
from threading import Thread
from time import sleep, time
from PyQt4 import QtNetwork, QtCore

__author__ = 'RoboCupULaval'


class UDPReceiving(QtCore.QThread):
    def __init__(self, name='UDP', ip='localhost', rcv_port=20021, snd_port=10021, debug=False):
        super().__init__()
        self._num = 0
        self._ip = ip
        self._default_rcv_port = 20021
        self._default_snd_port = 10021
        self._rcv_port = rcv_port
        self._snd_port = snd_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._is_running = False
        self._socket_is_up = False

        self._data = []
        self._msg_logging = []
        self._logger = logging.getLogger(name)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self.init_logger()

    def toggle_debug(self):
        print(self._logger.getEffectiveLevel())

    def init_logger(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    def send_message(self, p_object):
        if not type(b'') == type(p_object):
            self._logger.warn('SEND: object not serialized')
            p_object = pickle.dumps(p_object)
        self._logger.debug('SEND: {} bytes'.format(len(p_object)))
        try:
            self._sock.sendto(p_object, (self._ip, self._snd_port))
        except Exception as e:
            self._logger.error('Message not send : {}'.format(type(e).__name__ + e))

    def get_snd_port(self):
        self._logger.debug('GET: snd port {}'.format(self._snd_port))
        return self._snd_port

    def get_default_snd_port(self):
        self._logger.debug("GET: default snd port {}".format(self._default_snd_port))
        return self._default_snd_port

    def get_rcv_port(self):
        self._logger.debug('GET: rcv port {}'.format(self._rcv_port))
        return self._rcv_port

    def get_default_rcv_port(self):
        self._logger.debug('GET: default rcv port {}'.format(self._default_rcv_port))
        return self._default_rcv_port

    def set_snd_port(self, port):
        self._logger.debug('SET: snd port {} -> {}'.format(self._snd_port, port))
        self._snd_port = port

    def new_rcv_connexion(self, port):
        assert isinstance(port, int) and 0 < port
        self._logger.debug('NEW CONNEXION: port {}'.format(port))
        try:
            self.stop()
            self.wait_connexion()
            self.set_connexion(port)
            self.start()
        except Exception as e:
            self._logger.error('({}) {}'.format(type(e).__name__, e))

    def set_connexion(self, port):
        self._logger.debug('SET_CONNEXION: port {}'.format(port))
        self._rcv_port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self._logger.debug('START')
        self._is_running = True
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._ip, self._rcv_port))
        self._sock.settimeout(1)
        super().start()

    def stop(self):
        self._logger.debug('STOP')
        self._is_running = False

    def run(self):
        self._logger.debug('UP: {}, {}'.format(self._ip, self._rcv_port))
        self._socket_is_up = True
        while self._is_running:
            try:
                self._logger.debug("WAITING FOR: new package")
                data, addr = self._sock.recvfrom(65565)
                if not len(self._data) or not data == self._data[-1]:
                    data = self._num, data
                    self._data.append(data)
                    self._logger.debug("RECV {}: len {} from {}, {}".format(self._num, len(data[1]), addr[0], addr[1]))
                    self._num += 1
            except socket.timeout:
                self._logger.debug("TIMEOUT: recvfrom")
        self._socket_is_up = False
        self._sock.close()
        self._logger.debug('DOWN: {}, {}'.format(self._ip, self._rcv_port))

    def wait_connexion(self):
        self._logger.debug('WAITING FOR: Shutdown connexion: {}, {}'.format(self._ip, self._rcv_port))
        while self._socket_is_up:
            sleep(0.25)

    def get_last_data(self):
        raw_data = None
        try:
            raw_data = self._data.pop(0)
            self._logger.debug("GET: data {}".format(len(raw_data)))
        finally:
            return raw_data

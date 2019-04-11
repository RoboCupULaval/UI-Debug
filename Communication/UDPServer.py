# Under MIT License, see LICENSE.txt

import logging
import pickle
import socket
from queue import Queue
from threading import Thread, Event

__author__ = 'RoboCupULaval'


# FIXME Why do we have two UDPServer?  One is for Protobuf vision packet the other for StrategyIA communication
class UDPServer(Thread):
    def __init__(self, name='UDP', ip="127.0.0.1", rcv_port=None, snd_port=None, debug=False):
        super().__init__()
        self._num = 0
        self._ip = ip
        self.daemon = True
        self._default_rcv_port = 20021
        self._default_snd_port = 10221
        self._rcv_port = rcv_port or self._default_rcv_port
        self._snd_port = snd_port or self._default_snd_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._event_input = Event()
        self._event_connexion = Event()
        self._event_restart = Event()
        self._is_running = False

        self._data_queue = Queue()
        self._msg_logging = []
        self._logger = logging.getLogger(name)

        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)

        self.init_logger()

    def toggle_debug(self):
        pass

    def init_logger(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    def send_message(self, p_object):
        if not type(b'') == type(p_object):
            self._logger.debug('SEND: object not serialized')
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
            self.wait_for_new_connexion()
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
        self._event_restart.set()
        if not self.isAlive():
            super().start()

    def stop(self):
        self._logger.debug('STOP')
        self._is_running = False

    def run(self):
        while True:
            self._event_restart.wait()
            self._event_restart.clear()
            self._logger.debug('UP: {}, {}'.format(self._ip, self._rcv_port))
            self._event_connexion.clear()
            while self._is_running:
                try:
                    self._logger.debug("WAITING FOR: new package")
                    data, addr = self._sock.recvfrom(65565)
                    #if not len(self._data) or not data == self._data[-1]:
                    data = self._num, data
                    self._data_queue.put(data)
                    self._logger.debug("RECV {}: len {} from {}, {}".format(self._num, len(data[1]), addr[0], addr[1]))
                    self._num += 1
                    self._event_input.set()
                except socket.timeout:
                    self._logger.debug("TIMEOUT: recvfrom")
            self._sock.close()
            self._logger.debug('DOWN: {}, {}'.format(self._ip, self._rcv_port))
            self._event_connexion.set()

    def wait_for_new_connexion(self):
        self._logger.debug('WAITING FOR: Shutdown connexion: {}, {}'.format(self._ip, self._rcv_port))
        self._event_connexion.wait()

    def waiting_for_last_data(self):
        if self._data_queue.empty():
            self._logger.debug('WAITING FOR: Data in')
            self._event_input.wait()
        raw_data = None
        try:
            raw_data = self._data_queue.get()
            self._logger.debug("GET: data {}".format(len(raw_data)))
        finally:
            self._event_input.clear()
            return raw_data

# Under MIT License, see LICENSE.txt

import socket, pickle, time
from threading import Thread
from collections import deque

__author__ = 'RoboCupULaval'


class UDPSending(object):
    def __init__(self, p_ip='localhost', p_port=10021):
        self._ip = p_ip
        self._port = p_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, p_object):
        self._sock.sendto(pickle.dumps(p_object), (self._ip, self._port))


class UDPReceiving(object):
    def __init__(self, p_ip='localhost', p_port=20021):
        # Paramètres de connexion
        self._ip = p_ip
        self._port = p_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._thread = Thread(target=self._run)
        self._thread.daemon = True

        # Données
        self._data = deque(maxlen=100)

        # État
        self.is_running = False

    def start(self):
        """ Lance le serveur UDP à l'adresse et au port indiqué """
        self._sock.bind((self._ip, self._port))
        self.is_running = True
        self._thread.start()

    def _run(self):
        """ Boucle de réception de données """
        while self.is_running:
            try:
                data, addr = self._sock.recvfrom(1024)
                if not len(self._data) or not data == self._data[-1]:
                    data = pickle.loads(data)
                    self._data.append(data)
            except OSError:
                exit(-1)

    def stop(self):
        """ Arrête la boucle de réception """
        self.is_running = False

    def get_last_data(self):
        if len(self._data):
            return self._data[-1]

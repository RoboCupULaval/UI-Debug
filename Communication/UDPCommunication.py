# Under MIT License, see LICENSE.txt

import socket, pickle
from PyQt4.QtCore import QThread
from collections import deque

__author__ = 'RoboCupULaval'


class UDPSending(object):
    def __init__(self, ip='localhost', port=10021):
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, p_object):
        binaire = pickle.dumps(p_object)
        self._sock.sendto(binaire, (self._ip, self._port))


class UDPReceiving(object):
    def __init__(self, ip='localhost', port=20021):
        # Paramètres de connexion
        self._num = 0
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._thread = QThread()
        self._thread.run = self._run

        # Données
        #self._data = deque(maxlen=100)
        self._data = []

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
                data, addr = self._sock.recvfrom(65565)
                if not len(self._data) or not data == self._data[-1]:
                    data = self._num, data
                    self._data.append(data)
                    self._num += 1
            except OSError:
                exit(-1)

    def stop(self):
        """ Arrête la boucle de réception """
        self.is_running = False

    def get_last_data(self):
        if len(self._data):
            return self._data.pop(0)

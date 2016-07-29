# Under MIT License, see LICENSE.txt

import pickle
import socket
from PyQt4 import QtNetwork, QtCore

__author__ = 'RoboCupULaval'


class UDPSending(object):
    def __init__(self, ip='localhost', port=10021):
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, p_object):
        if isinstance(p_object, dict):
            p_object = pickle.dumps(p_object)
        self._sock.sendto(p_object, (self._ip, self._port))


class UDPServer(QtCore.QThread):
    def __init__(self, parent=None, port=20021):
        super().__init__(parent)
        self.prnt = parent
        self._udp_socket = QtNetwork.QUdpSocket()
        self._udp_socket.bind(QtNetwork.QHostAddress.LocalHost, port)
        self._udp_socket.readyRead.connect(self.read_udp)
        self.connect(self._udp_socket,
                     QtCore.SIGNAL('readyRead()'),
                     self,
                     QtCore.SIGNAL('read_upd()'))

        self.STOP = False
        self._mutex = QtCore.QMutex()
        self._num = 0
        self._data = []

    def run(self):
        """ Connexion et autres """

        while True:
            if self._udp_socket is not None and \
               self._udp_socket.state() == QtNetwork.QAbstractSocket.BoundState:
                self._udp_socket.waitForReadyRead(1000)
            else:
                self.msleep(100)
            if self.STOP and self._udp_socket is not None:
                self._udp_socket.close()
                break

    def stop(self):
        QtCore.QMutexLocker(self._mutex).relock()
        self.STOP = True
        QtCore.QMutexLocker(self._mutex).unlock()

    def read_udp(self):
        while self._udp_socket.hasPendingDatagrams():
            datagram, host, port = self._udp_socket.readDatagram(self._udp_socket.pendingDatagramSize())
            self._data.append(datagram)
            self._num += 1

    def get_last_data(self):
        """ Requête externe afin d'avoir accès aux données récupérées """
        raw_data = None
        try:
            raw_data = self._data.pop(0)
        finally:
            return raw_data

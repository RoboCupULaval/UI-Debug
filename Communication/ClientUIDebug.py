# Under MIT License, see LICENSE.txt

from .UDPServer import UDPServer

__author__ = 'RoboCupULaval'


class ClientUIDebug(object):
    def __init__(self, name, port_sender=20021, port_receiver=10021):
        self._name = str(name)
        self._udp = UDPServer(snd_port=port_sender, rcv_port=port_receiver)

    def start(self):
        self._udp.start()

    # Méthode d'initialisation de l'UI Debug
    def init_tactics(self, list_tactics):
        data = {'name': self._name, 'type': 10, 'data': {'T': list_tactics}}
        self._udp.send_message(data)

    # Méthode d'envoie de commande
    def send_message_log(self, message, level=2):
        data = {'name': self._name, 'type': 2, 'data': {'level': level, 'message': message}}
        self._udp.send_message(data)

    # Requête de dernière commande
    def get_last_command(self):
        return self._udp.get_last_data()

# Under MIT License, see LICENSE.txt

from Communication.UDPCommunication import UDPSending, UDPReceiving

__author__ = 'RoboCupULaval'


class ClientUIDebug(object):
    def __init__(self, name, port_sender=20021, port_receiver=10021):
        self._name = str(name)
        self._udp_sender = UDPSending(port=port_sender)
        self._udp_receiver = UDPReceiving(port=port_receiver)

    def start(self):
        self._udp_receiver.start()

    # Méthode d'initialisation de l'UI Debug
    def init_tactics(self, list_tactics):
        data = {'name': self._name, 'type': 10, 'STA': {'T': list_tactics}}
        self._udp_sender.send_message(data)

    # Méthode d'envoie de commande
    def send_message_log(self, message, level=2):
        data = {'name': self._name, 'type': 2, 'data': {'level': level, 'message': message}}
        self._udp_sender.send_message(data)

    # Requête de dernière commande
    def get_last_command(self):
        return self._udp_receiver.get_last_data()

# Under MIT License, see LICENSE.txt

from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'

UI
class DataOutModel(object):
    def __init__(self):
        self._name = 'UI'
        self._version = 'v1.0'
        self._udp_sender = UDPSending()
        self.target = (0, 0)

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0)):
        package = self.get_empty_package()
        package['type'] = 5002
        package['link'] = id_bot
        package['data'] = {'tactic': tactic, 'target': target, 'goal': goal}
        self._udp_sender.send_message(package)

    def send_strat(self, strat):
        package = self.get_empty_package()
        package['type'] = 5001
        package['data'] = {'strategy': strat}
        self._udp_sender.send_message(package)

    def get_empty_package(self):
        return {'name': self._name, 'type': None, 'data': None, 'version': self._version, 'link': None}

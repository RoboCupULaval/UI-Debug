# Under MIT License, see LICENSE.txt

from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'


class DataOutModel(object):
    def __init__(self):
        self._udp_sender = UDPSending()
        self.target = (0, 0)

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0)):
        self._udp_sender.send_message({'tactic': {'id': id_bot, 'tactic': tactic, 'target': target, 'goal': goal}})

    def send_strat(self, strat):
        self._udp_sender.send_message({'strategy': strat})

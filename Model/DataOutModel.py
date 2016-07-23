# Under MIT License, see LICENSE.txt

from PyQt4.QtCore import QTimer
from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'


class DataOutModel:
    def __init__(self, controller=None):
        self._controller = controller
        self._name = 'UI'
        self._version = 'v1.0'
        self._udp_sender = UDPSending()
        self.target = (0, 0)

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_screen)
        self.frame_timer.start(20)

    def update_screen(self):
        self._controller.update_target_on_screen()

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0)):
        package = self.get_empty_package()
        package['type'] = 5003
        package['link'] = id_bot
        package['data'] = {'tactic': tactic, 'target': target, 'goal': goal}
        self._udp_sender.send_message(package)

    def send_strat(self, strat):
        package = self.get_empty_package()
        package['type'] = 5002
        package['data'] = {'strategy': strat}
        self._udp_sender.send_message(package)

    def send_toggle_human_control(self, result):
        package = self.get_empty_package()
        package['type'] = 5001
        package['data'] = {'is_human_control': result}
        self._udp_sender.send_message(package)

    def get_empty_package(self):
        return {'name': self._name, 'type': None, 'data': None, 'version': self._version, 'link': None}

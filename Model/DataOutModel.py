# Under MIT License, see LICENSE.txt

from PyQt4.QtCore import QTimer
from Model.DataObject.SendingData.SendingStrategy import SendingStrategy
from Model.DataObject.SendingData.SendingToggleHumanCtrl import SendingToggleHumanCtrl
from Model.DataObject.SendingData.SendingTactic import SendingTactic

__author__ = 'RoboCupULaval'


class DataOutModel:
    def __init__(self, controller=None):
        self._controller = controller
        self._udp_sender = None
        self.target = 0, 0

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_screen)
        self.frame_timer.start(20)

    def setup_udp_server(self, server):
        self._udp_sender = server

    def update_screen(self):
        self._controller.update_target_on_screen()

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0)):
        target = int(target[0]), int(target[1])
        goal = int(goal[0]), int(goal[1])
        pkg = SendingTactic().set_data(tactic=tactic,
                                       id=id_bot % 6,
                                       target=target,
                                       goal=goal)
        self._udp_sender.send_message(pkg.get_binary())

    def send_strategy(self, strat):
        pkg = SendingStrategy().set_data(strategy=strat)
        self._udp_sender.send_message(pkg.get_binary())

    def send_toggle_human_control(self, result):
        pkg = SendingToggleHumanCtrl().set_data(is_human_control=result)
        self._udp_sender.send_message(pkg.get_binary())

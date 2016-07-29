# Under MIT License, see LICENSE.txt

from PyQt4.QtCore import QTimer
from Communication.UDPCommunication import UDPSending
from Model.DataModel.SendingData.SendingStrategy import SendingStrategy
from Model.DataModel.SendingData.SendingToggleHumanCtrl import SendingToggleHumanCtrl
from Model.DataModel.SendingData.SendingTactic import SendingTactic

__author__ = 'RoboCupULaval'


class DataOutModel:
    def __init__(self, controller=None):
        self._controller = controller
        self._udp_sender = UDPSending()
        self.target = 0, 0

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_screen)
        self.frame_timer.start(20)

    def update_screen(self):
        self._controller.update_target_on_screen()

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0)):
        pkg = SendingTactic().set_data(tactic=tactic,
                                       id=id_bot,
                                       target=target,
                                       goal=goal)
        self._udp_sender.send_message(pkg.get_binary())

    def send_strategy(self, strat):
        pkg = SendingStrategy().set_data(strategy=strat)
        self._udp_sender.send_message(pkg.get_binary())

    def send_toggle_human_control(self, result):
        pkg = SendingToggleHumanCtrl().set_data(is_human_control=result)
        self._udp_sender.send_message(pkg.get_binary())

# Under MIT License, see LICENSE.txt

from PyQt5.QtCore import QTimer
from Model.DataObject.SendingData.SendingStrategy import SendingStrategy
from Model.DataObject.SendingData.SendingToggleHumanCtrl import SendingToggleHumanCtrl
from Model.DataObject.SendingData.SendingTactic import SendingTactic
from Model.DataObject.SendingData.SendingHandShake import SendingHandShake
from Model.DataObject.SendingData.SendingGeometry import SendingGeometry

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

    def send_strategy(self, strat, team):
        pkg = SendingStrategy().set_data(strategy=strat, team=team)
        self._udp_sender.send_message(pkg.get_binary())

    def send_toggle_human_control(self, result):
        pkg = SendingToggleHumanCtrl().set_data(is_human_control=result)
        self._udp_sender.send_message(pkg.get_binary())

    def send_handshake(self):
        pkg = SendingHandShake()
        self._udp_sender.send_message(pkg.get_binary())

    def send_geometry(self, field_control):
        pkg = SendingGeometry().set_data(width=field_control.width,
                                         height=field_control.height,
                                         center_radius=field_control.center_radius,
                                         defense_radius=field_control.defense_radius,
                                         defense_stretch=field_control.defense_stretch,
                                         goal_width=field_control.goal_width,
                                         goal_height=field_control.goal_height)
        if self._udp_sender is not None:
            self._udp_sender.send_message(pkg.get_binary())

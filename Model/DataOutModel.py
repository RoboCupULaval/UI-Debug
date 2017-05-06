# Under MIT License, see LICENSE.txt

from PyQt5.QtCore import QTimer
from Model.DataObject.SendingData.SendingStrategy import SendingStrategy
from Model.DataObject.SendingData.SendingToggleHumanCtrl import SendingToggleHumanCtrl
from Model.DataObject.SendingData.SendingTactic import SendingTactic
from Model.DataObject.SendingData.SendingHandShake import SendingHandShake
from Model.DataObject.SendingData.SendingGeometry import SendingGeometry
from Model.DataObject.SendingData.SendingAIServer import SendingAIServer
from Model.DataObject.SendingData.SendingDataPorts import SendingDataPorts
from Model.DataObject.SendingData.SendingUDPConfig import SendingUDPConfig

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

    def send_tactic(self, id_bot, tactic, target=(0, 0), goal=(0, 0), args=None):
        target = int(target[0]), int(target[1])
        goal = int(goal[0]), int(goal[1])
        if args is None:
            args = []
        pkg = SendingTactic().set_data(tactic=tactic,
                                       id=id_bot % 6,
                                       target=target,
                                       goal=goal,
                                       args=args)
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
        pkg = SendingGeometry().set_data(field_length=field_control.field_length,
                                         field_width=field_control.field_width,
                                         center_circle_radius=field_control.center_circle_radius,
                                         defense_radius=field_control.defense_radius,
                                         defense_stretch=field_control.defense_stretch,
                                         goal_width=field_control.goal_width,
                                         goal_depth=field_control.goal_depth,
                                         ratio_field_mobs=field_control.ratio_field_mobs)
        if self._udp_sender is not None:
            self._udp_sender.send_message(pkg.get_binary())

    def send_ports_rs(self, ports_info):
        pkg = SendingDataPorts().set_data(recv_port=ports_info['recv_port'],
                                          send_port=ports_info['send_port'])
        if self._udp_sender is not None:
            self._udp_sender.send_message(pkg.get_binary())

    def send_server(self, server_info):
        pkg = SendingAIServer().set_data(is_serial=server_info['is_serial'],
                                         ip=server_info['ip'],
                                         port=server_info['port'])
        if self._udp_sender is not None:
            self._udp_sender.send_message(pkg.get_binary())

    def send_udp_config(self, udp_config_info):
        pkg = SendingUDPConfig().set_data(ip=udp_config_info['ip'],
                                         port=int(udp_config_info['port']))
        if self._udp_sender is not None:
            self._udp_sender.send_message(pkg.get_binary())
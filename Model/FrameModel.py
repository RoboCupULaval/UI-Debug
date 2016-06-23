# Under MIT License, see LICENSE.txt

from collections import deque

from PyQt4.QtCore import *

from Communication.vision import Vision
from Controller.FieldController import FieldController

__author__ = 'RoboCupULaval'


class FrameModel(object):
    # TODO : Revoir le modèle pour le rendre standard à Qt
    def __init__(self, controller):
        self._controller = controller
        self.field_info = FieldController()
        self.receive_data_queue = deque(maxlen=100)
        self.send_data_queue = deque(maxlen=100)
        self.row_header = list()
        self.col_header = list()

        self.vision = Vision()

        self.frame_catcher_stop = False

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.catch_frame)
        self.frame_timer.start(20)

    def catch_frame(self):
        if not self.frame_catcher_stop:
            frame = self.vision.get_latest_frame()
            if frame is None:
                pass
            elif len(self.receive_data_queue) == 0 or not frame.detection.frame_number == self.receive_data_queue[-1].detection.frame_number:
                self.update_data(frame)

    def update_data(self, frame):
        self.receive_data_queue.append(frame)
        # Mise à jour des données de la balle
        try:
            x = self.receive_data_queue[-1].detection.balls[0].x
            y = self.receive_data_queue[-1].detection.balls[0].y
            self._controller.set_ball_pos_on_screen(x, y)
        except BaseException:
            self._controller.hide_mob()

        # Mise à jour des données de l'équipe jaune
        try:
            list_bot_id = {0, 1, 2, 3, 4, 5}
            for info_bot in self.receive_data_queue[-1].detection.robots_yellow:
                list_bot_id.remove(info_bot.robot_id)
                bot_id = info_bot.robot_id
                x = info_bot.x
                y = info_bot.y
                theta = info_bot.orientation
                self._controller.set_robot_pos_on_screen(bot_id, (x, y), theta)

            for bot_id in list_bot_id:
                self._controller.hide_mob(bot_id)
        except BaseException:
            pass

        # Mise à jour des données de l'équipe blue
        try:
            list_bot_id = {0, 1, 2, 3, 4, 5}
            for info_bot in self.receive_data_queue[-1].detection.robots_blue:
                list_bot_id.remove(info_bot.robot_id)
                bot_id = info_bot.robot_id
                x = info_bot.x
                y = info_bot.y
                theta = info_bot.orientation
                self._controller.set_robot_pos_on_screen(bot_id + 6, (x, y), theta)

            for bot_id in list_bot_id:
                self._controller.hide_mob(bot_id + 6)
        except BaseException:
            pass


    def is_connected(self):
        if len(self.receive_data_queue) > 0:
            return True
        return False
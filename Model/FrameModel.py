# Under MIT License, see LICENSE.txt

from collections import deque
from datetime import datetime
from datetime import timedelta

from PyQt4.QtCore import QTimer

from Communication.vision import Vision

__author__ = 'RoboCupULaval'


class FrameModel(object):
    """ FrameModel est un modèle qui gère les données provenant du système de vision. FrameModel possède
        un récupérateur de données du module de vision (Frame Catcher) pour ensuite mettre à jour les
        positions des objets mobiles sur la vue du terrain (Screen View). """
    def __init__(self, controller):
        self._controller = controller
        self._vision = Vision()

        # Initialisation des variables de données
        self._max_data_queue = 100
        self._data_queue_received = deque(maxlen=self._max_data_queue)

        # Initialisation des variables pour le frame catcher
        self._last_frame_catched_time = datetime.min
        self._frame_catcher_update_rate = 30.0        # Fréquence d'update en Hz
        self._frame_catcher_timer = QTimer()
        self._init_frame_catcher()

    def _init_frame_catcher(self):
        """ Initialise le timer pour récupérer """
        self._frame_catcher_timer.timeout.connect(self._catching_frame)
        self._frame_catcher_timer.start(1 / self._frame_catcher_update_rate)

    def _catching_frame(self):
        """ Récupère le dernier frame reçu, le met à jour et le sauvegarde """
        if datetime.now() - self._last_frame_catched_time > timedelta(seconds=1 / self._frame_catcher_update_rate):
            frame = self._vision.get_latest_frame()
            if frame is not None and \
               (len(self._data_queue_received) == 0 or not
                    frame.detection.frame_number == self._data_queue_received[-1].detection.frame_number):
                self._last_frame_catched_time = datetime.now()
                self._update_view_screen_mobs(frame)

    def _update_view_screen_mobs(self, frame):
        """ Mise à jour des données de la vue de la balle et des robots """
        self._data_queue_received.append(frame)
        # Mise à jour des données de la balle
        try:
            x = self._data_queue_received[-1].detection.balls[0].x
            y = self._data_queue_received[-1].detection.balls[0].y
            self._controller.set_ball_pos_on_screen(x, y)
        except BaseException:
            self._controller.hide_mob()

        # Mise à jour des données de l'équipe jaune
        try:
            list_bot_id = {0, 1, 2, 3, 4, 5}
            for info_bot in self._data_queue_received[-1].detection.robots_yellow:
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
            for info_bot in self._data_queue_received[-1].detection.robots_blue:
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
        """ Détermine si le modèle a reçu des données de la vision depuis au moins 1 seconde """
        if datetime.now() - self._last_frame_catched_time < timedelta(seconds=1):
            return True
        return False

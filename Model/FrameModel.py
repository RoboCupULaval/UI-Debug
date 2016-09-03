# Under MIT License, see LICENSE.txt

from collections import deque
from datetime import datetime
from datetime import timedelta

from PyQt4.QtCore import QTimer

__author__ = 'RoboCupULaval'


class FrameModel:
    """
        FrameModel est un modèle qui gère les données provenant du système de vision. FrameModel possède
        un récupérateur de données du module de vision (Frame Catcher) pour ensuite mettre à jour les
        positions des objets mobiles sur la vue du terrain (Screen View).
    """
    def __init__(self, controller=None):
        self._controller = controller
        self._vision = None
        self._recorder = None

        # Initialisation des variables de données
        self._max_data_queue = 3000
        self._data_queue_received = deque(maxlen=self._max_data_queue)
        self._current_frame = None

        # Initialisation des variables pour le frame catcher
        self._last_frame_caught_time = datetime.min
        self._frame_catcher_update_rate = 60.0        # Fréquence d'update en Hz
        self._frame_catcher_timer = QTimer()

        # Contrôleur
        self._recorder_is_enable = False

    def set_vision(self, server):
        self._vision = server

    def start(self):
        """ Initialise le timer pour récupérer """
        self._frame_catcher_timer.timeout.connect(self._catching_frame)
        self._frame_catcher_timer.start(self._frequency_to_milliseconds_int(self._frame_catcher_update_rate))

    def _update_is_in_progress(self):
        """ Vérifie si la mise à jour des données est terminée pour éviter une erreur de récursivité """
        if datetime.now() - self._last_frame_caught_time > timedelta(seconds=1 / self._frame_catcher_update_rate):
            return False
        else:
            return True

    def _frame_has_been_processed(self, frame):
        """ Vérifie si un frame a été traité ou non """
        if frame is None:
            return True
        if len(self._data_queue_received) == 0 or not frame.detection.frame_number == self._current_frame.detection.frame_number:
            return False
        return True

    def _catching_frame(self):
        """ Récupère le dernier frame reçu, le met à jour et le sauvegarde """
        if not self._update_is_in_progress():
            frame = self._get_last_frame()
            if not self._frame_has_been_processed(frame):
                self._last_frame_caught_time = datetime.now()
                self._update_view_screen_mobs(datetime.now(), frame)

    def _get_last_frame(self):
        """ Récupère le dernier frame de la vision ou de l'enregistreur """
        if not self._recorder_is_enable:
            return self._vision.get_latest_frame()
        else:
            return self._recorder.get_last_frame()

    def _update_view_screen_mobs(self, ftime, frame):
        """ Mise à jour des données de la vue des objets mobiles  """
        if not self._recorder_is_enable:
            frame_pkg = ftime, frame
            self._data_queue_received.append(frame_pkg)
        self._current_frame = frame
        self._update_view_screen_ball()
        self._update_view_screen_team_yellow()
        self._update_view_screen_team_blue()

    def _update_view_screen_ball(self):
        """ Muse à jour des données de la vue de la balle """
        try:
            x = self._current_frame.detection.balls[0].x
            y = self._current_frame.detection.balls[0].y
            self._controller.set_ball_pos_on_screen(x, y)
        except Exception as e:
            self._controller.hide_mob()

    def _update_view_screen_team_yellow(self):
        """ Muse à jour des données de la vue des robots de l'équipe jaune """
        try:
            list_bot_id = {0, 1, 2, 3, 4, 5}
            for info_bot in self._current_frame.detection.robots_yellow:
                list_bot_id.remove(info_bot.robot_id)
                bot_id = info_bot.robot_id
                x = info_bot.x
                y = info_bot.y
                theta = info_bot.orientation
                self._controller.set_robot_pos_on_screen(bot_id, (x, y), theta)

            for bot_id in list_bot_id:
                self._controller.hide_mob(bot_id)
        except Exception as e:
            pass

    def _update_view_screen_team_blue(self):
        """ Muse à jour des données de la vue des robots de l'équipe bleue """
        try:
            list_bot_id = {0, 1, 2, 3, 4, 5}
            for info_bot in self._current_frame.detection.robots_blue:
                list_bot_id.remove(info_bot.robot_id)
                bot_id = info_bot.robot_id
                x = info_bot.x
                y = info_bot.y
                theta = info_bot.orientation
                self._controller.set_robot_pos_on_screen(bot_id + 6, (x, y), theta)

            for bot_id in list_bot_id:
                self._controller.hide_mob(bot_id + 6)
        except Exception as e:
            pass

    def enable_recorder(self):
        """ Activer l'enregistreur sur le modèle de frame """
        if self._recorder is not None:
            self._recorder.init(frames=self._data_queue_received)
            self._recorder_is_enable = True

    def disable_recorder(self):
        """ Désactiver l'enregistreur sur le modèle de frame """
        if self._recorder is not None:
            self._recorder_is_enable = False

    def is_connected(self):
        """ Détermine si le modèle a reçu des données de la vision depuis au moins 1 seconde """
        if datetime.now() - self._last_frame_caught_time < timedelta(seconds=1):
            return True
        return False

    def set_recorder(self, ref_recorder):
        """ Assigne la référence de l'enregistreur une seule fois """
        if self._recorder is None:
            self._recorder = ref_recorder

    @staticmethod
    def _frequency_to_milliseconds_int(frequency):
        """ Convertit une fréquence en millisecondes en format int """
        return 1 / frequency * 1000

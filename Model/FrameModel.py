# Under MIT License, see LICENSE.txt

from collections import deque
from datetime import datetime
from datetime import timedelta

from PyQt5.QtCore import QTimer

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
                #print(frame.geometry)
                if frame.geometry.field.line_width !=0:
                    self._update_field_size(frame)


    def _get_last_frame(self):
        """ Récupère le dernier frame de la vision ou de l'enregistreur """
        if not self._recorder_is_enable:
            try:
                return self._vision.get_latest_frame()
            except:
                return self._recorder.get_last_frame()
        else:
            return self._recorder.get_last_frame()

    def _update_field_size(self, frame):
        """ Mise à jour des données de dimensions du terrain"""
        self._controller.set_field_size(frame.geometry.field)

    def _update_view_screen_mobs(self, ftime, frame):
        """ Mise à jour des données de la vue des objets mobiles  """
        if not self._recorder_is_enable:
            frame_pkg = ftime, frame
            self._data_queue_received.append(frame_pkg)
        self._current_frame = frame
        self._update_view_screen_ball()
        list_blue_bot_id = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}  # TODO : Créer une variable globale
        self._update_view_screen_robot(list_blue_bot_id, 'yellow')
        list_yellow_bot_id = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        self._update_view_screen_robot(list_yellow_bot_id, 'blue')

    def _update_view_screen_ball(self):
        """ Mise à jour des données de la vue de la balle """
        try:
            x = self._current_frame.detection.balls[0].x
            y = self._current_frame.detection.balls[0].y
            self._controller.set_ball_pos_on_screen(x, y)
        except Exception as e:
            self._controller.hide_mob()

    def _update_view_screen_robot(self, list_id, team_color):
        """ Mise à jour des données de la vue des robots"""

        try:
            if team_color == 'yellow':
                detected_robots = self._current_frame.detection.robots_yellow
            elif team_color == 'blue':
                detected_robots = self._current_frame.detection.robots_blue

            for info_bot in detected_robots:
                list_id.remove(info_bot.robot_id)
                bot_id = info_bot.robot_id
                x = info_bot.x
                y = info_bot.y
                theta = info_bot.orientation
                self._controller.set_robot_pos_on_screen(bot_id, team_color, (x, y), theta)

            for bot_id in list_id:
                self._controller.hide_mob(bot_id, team_color)
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

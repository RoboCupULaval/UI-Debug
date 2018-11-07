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
        self._max_data_queue = 1
        self._data_queue_received = deque(maxlen=self._max_data_queue)
        self._current_frame = None

        # Initialisation des variables pour le frame catcher
        self._last_frame_caught_time = datetime.min
        self._frame_catcher_update_rate = 100.0        # Fréquence d'update en Hz
        self._frame_catcher_timer = QTimer()

        self._ball_last_detected_time = datetime.min
        self._robots_last_detected_time = {'blue': {}, 'yellow': {}}

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


    def _catching_frame(self):
        """ Récupère le dernier frame reçu, le met à jour et le sauvegarde """
        if not self._update_is_in_progress():
            frames = self._get_last_frames()
            #if not self._frame_has_been_processed(frame):
            for frame in frames:
                # if len(frame.geometry.calib) > 0:
                #     for c in frame.geometry.calib:
                #         print(c.camera_id, c.tx, c.ty)
                self._last_frame_caught_time = datetime.now()
                self._update_view_screen_mobs(datetime.now(), frame)
                if frame.geometry.field.field_width != 0:
                    self._update_field_size(frame)


    def _get_last_frames(self):
        """ Récupère le dernier frame de la vision ou de l'enregistreur """
        if not self._recorder_is_enable:
            return self._vision.get_latest_frames()
        else:
            return [self._recorder.get_last_frame()]

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

        self._update_view_screen_robot('blue')
        self._update_view_screen_robot('yellow')

    def _update_view_screen_ball(self):
        """ Mise à jour des données de la vue de la balle """
        balls = self._current_frame.detection.balls
        if len(balls) > 0:
            self._ball_last_detected_time = datetime.now()
            self._controller.set_ball_pos_on_screen(balls[0].x, balls[0].y)

        # Only one frame out of 4 have the ball's geometry
        if datetime.now() - self._ball_last_detected_time > timedelta(seconds=1):
            self._controller.hide_ball()

    def _update_view_screen_robot(self, team_color):
        """ Mise à jour des données de la vue des robots"""

        if team_color == 'yellow':
            detected_robots = self._current_frame.detection.robots_yellow
        elif team_color == 'blue':
            detected_robots = self._current_frame.detection.robots_blue

        for info_bot in detected_robots:
            bot_id = info_bot.robot_id
            x = info_bot.x
            y = info_bot.y
            theta = info_bot.orientation
            self._controller.set_robot_pos_on_screen(bot_id, team_color, (x, y), theta)
            self._robots_last_detected_time[team_color][bot_id] = datetime.now()

        for id, last_detection_time in self._robots_last_detected_time[team_color].items():
            if datetime.now() - last_detection_time > timedelta(seconds=1):
                self._controller.hide_mob(id, team_color)


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

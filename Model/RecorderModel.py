# Under MIT License, see LICENSE.txt

import logging
from datetime import datetime, timedelta

__author__ = 'RoboCupULaval'


def recorder_checker(func):

        def check_installed(*args, **kwargs):
            if RecorderModel.is_installed:
                return func(*args, **kwargs)
            else:
                return None

        return check_installed


class RecorderModel:
    is_installed = False

    def __init__(self, debug=False):
        """
            RecorderModel
        """
        self._logger = logging.getLogger(RecorderModel.__name__)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)

        # === DATA ===
        self._data_frames = None
        self._game_state = None
        self._robot_state = None

        self._cursor_pst = None
        self._nb_frame = None

        # === TIME ===
        self._time_lapse = timedelta(seconds=30)
        self._time_max = None
        self._time_min = None
        self._last_req_time = None

        # === CTRL ===
        self._ctrl_play = False

        # == INIT ==
        self._init_logger()

    # === INIT ===
    def init(self, **kwargs):
        """ Initialise le Recorder """
        if 'frames' in kwargs.keys():
            self._init_time_var(kwargs['frames'][-1][0])
            self._init_frames(kwargs['frames'])
            self._logger.debug('INIT: frames')

        if 'game_state' in kwargs.keys() and 'robot_state' in kwargs.keys():
            self._init_states(kwargs['game_state'], kwargs['robot_state'])
            self._logger.debug('INIT: game_state and robot_state')

        if self._data_frames is not None and self._game_state is not None and self._robot_state is not None:
            RecorderModel.is_installed = True

    def _init_frames(self, data_frame):
        """ Initialise les paramètres de données """
        data_frame = list(data_frame)
        self._nb_frame = self._get_limit_frame_number(data_frame)
        # DATA SAVE
        self._data_frames = data_frame[self._nb_frame:]

        self._cursor_pst = self._nb_frame
        self._last_req_time = datetime.now()

    def _init_states(self, game_state, robot_state):
        self._game_state = game_state
        self._robot_state = robot_state

    def _init_time_var(self, p_time):
        """ Initialise les paramètres de temps """
        self._time_max = p_time
        self._time_min = self._time_max - self._time_lapse

    def _init_logger(self):
        """ Initialisation du logger """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.debug('INIT: Logger')

    # === GETTER / SETTER ===
    def _get_limit_frame_number(self, data):
        """ Récupère le nombre de frame en fonction du laps de temps """
        iterator = -1
        while True:
            try:
                if data[iterator][0] < self._time_min:
                    return iterator
            except IndexError:
                iterator += 1
                self._time_min = data[iterator][0]
                return iterator
            iterator -= 1

    # === PUBLIC METHOD ===
    @recorder_checker
    def play(self):
        """ Met le Recorder en mode lecture """
        self._ctrl_play = True

    @recorder_checker
    def pause(self):
        """ Met le Recorder en mode pause """
        self._ctrl_play = False

    @recorder_checker
    def back(self):
        """ Recule le cursor d'un frame """
        index = self._cursor_pst - 1
        if index >= self._nb_frame:
            self._cursor_pst = index

    @recorder_checker
    def rewind(self):
        """ Recule le cursor au début """
        self._cursor_pst = self._nb_frame

    @recorder_checker
    def forward(self):
        """ Avance le curseur d'un frame """
        index = self._cursor_pst + 1
        if index <= -1:
            self._cursor_pst = index

    @recorder_checker
    def skip_to(self, percentage):
        """ Met le Recorder une position spécifique """
        index = self._nb_frame - self._nb_frame * percentage / 100
        self._cursor_pst = int(index)

    @recorder_checker
    def get_last_frame(self):
        """ Recupère le frame en fonction du curseur de lecture du Recorder """
        if not self._ctrl_play:
            self._last_req_time = datetime.now()
            return self._data_frames[self._cursor_pst][1]
        else:
            if self._cursor_pst == -1:
                self._last_req_time = datetime.now()
                return self._data_frames[-1][1]
            else:
                dt_frame = self._data_frames[self._cursor_pst + 1][0] - self._data_frames[self._cursor_pst][0]
                dt_get = datetime.now() - self._last_req_time
                if dt_get > dt_frame:
                    self._last_req_time = datetime.now()
                    self._cursor_pst += 1
                return self._data_frames[self._cursor_pst][1]

    @recorder_checker
    def get_game_state(self):
        if self._last_req_time is not None:
            return self._game_state[self._data_frames[self._cursor_pst][0]]
        else:
            return self._game_state[-1]

    @recorder_checker
    def get_robot_state(self):
        if self._last_req_time is not None:
            return self._robot_state[self._data_frames[self._cursor_pst][0]]
        else:
            return self._robot_state[-1]

    @recorder_checker
    def get_cursor_percentage(self):
        """ Recupère le pourcentage de frame """
        if self._cursor_pst is not None and self._nb_frame is not None:
            value = 100 - (self._cursor_pst + 1) / self._nb_frame * 100
            return value
        else:
            return 0

    def is_playing(self):
        return self._ctrl_play

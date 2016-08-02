# Under MIT License, see LICENSE.txt

__author__ = 'RoboCupULaval'


class RecorderModel:
    def __init__(self):
        """
            RecorderModel
        """
        self.is_installed = False

        # === DATA ===
        self._data_frames = None
        self._current_frame = None
        self._nb_frame = None

        # === TIME ===
        self._time_lapse = 30
        self._time_max = None
        self._time_min = None
        self._last_time = None

        # === CTRL ===
        self._ctrl_play = False

    # === INIT ===
    def init(self, data):
        """ Initialise le Recorder """
        self._init_time_var(data[-1].time)
        self._init_data(data)

    def _init_data(self, data):
        """ Initialise les paramètres de données """
        self._nb_frame = self._get_limit_frame_number(data)
        self._data_frames = data[self._nb_frame:]
        self._current_frame = -1, data[-1]

    def _init_time_var(self, p_time):
        """ Initialise les paramètres de temps """
        self._time_max = p_time
        self._time_min = self._time_max - self._time_lapse

    # === GETTER / SETTER ===
    def _get_limit_frame_number(self, data):
        """ Récupère le nombre de frame en fonction du laps de temps """
        iterator = -1
        while True:
            try:
                if data[iterator].time < self._time_min:
                    return iterator
            except IndexError:
                iterator += 1
                self._time_min = data[iterator].time
                return iterator
            iterator -= 1

    # === PUBLIC METHOD ===
    def play(self):
        """ Met le Recorder en mode lecture """
        self._ctrl_play = True

    def pause(self):
        """ Met le Recorder en mode pause """
        self._ctrl_play = False

    def forback(self):
        """ Recule le cursor d'un frame """
        try:
            index = self._current_frame[0] - 1
            self._current_frame = index, self._data_frames[index]
        except IndexError:
            pass

    def forward(self):
        """ Avance le curseur d'un frame """
        try:
            index = self._current_frame[0] + 1
            if index <= -1:
                self._current_frame = index, self._data_frames[index]
        except IndexError:
            pass

    def skip_to(self, percentage):
        """ Met le Recorder une position spécifique """
        index = self._nb_frame - self._nb_frame * percentage / 100 - 1
        self._current_frame = index, self._data_frames[index]

    def get_last_frame(self):
        """ Recupère le frame en fonction du curseur de lecture du Recorder """
        # TODO - Implemented RecorderModel.get_last_frame
        pass

    def get_cursor_percentage(self):
        """ Recupère le pourcentage de frame """
        return self._current_frame[0] / self._nb_frame * 100

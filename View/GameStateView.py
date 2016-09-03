# Under MIT License, see LICENSE.txt

import logging
from threading import Thread
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt

__author__ = 'RoboCupULaval'


class GameStateView(QWidget):
    def __init__(self, controller=None, debug=False):
        super().__init__(controller)
        self._logger = logging.getLogger(GameStateView.__name__)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self._logger.debug('CONSTRUCT: Begin...')
        self._ctrl = controller

        # UI
        self._layout = QGridLayout()

        # CORE SYSTEM
        self._robot_state_loop = Thread()
        self._game_state_loop = Thread()

        # INITIALIZATION
        self.init_logger()
        self.init_ui()
        self.init_loop()
        self.hide()
        self._logger.debug('CONSTRUCT: ... End')

    def _get_style_sheet(self, is_yellow=None, bold=False, color='black'):
        param_sheet = ' ; '.join(['color:{}'.format(color),
                                'border-style: solid',
                                'border-color: black',
                                'border-width: 1px'])
        if is_yellow is not None:
            if is_yellow:
                color = '#ffff88'
            else:
                color = '#8888ff'
            param_sheet += ' ; background: {}'.format(color)

        if bold:
            param_sheet += ' ; font-weight: bold'

        return 'QLabel {' + param_sheet + '}'

    def init_logger(self):
        """ Initialisation du logger """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.debug('INIT: Logger')

    def init_ui(self):
        self._logger.debug('INIT: UI')
        self.setLayout(self._layout)
        self._layout.setVerticalSpacing(0)
        self._layout.setHorizontalSpacing(0)

        # Main header
        label_blue_team = QLabel('Équipe Bleue')
        label_blue_team.setMargin(5)
        label_blue_team.setAlignment(Qt.AlignCenter)
        label_blue_team.setStyleSheet(self._get_style_sheet(is_yellow=False))
        self._layout.addWidget(label_blue_team, 1, 1)

        self._label_strat_blue = QLabel('None')
        self._label_strat_blue.setMargin(5)
        self._label_strat_blue.setAlignment(Qt.AlignCenter)
        self._label_strat_blue.setStyleSheet(self._get_style_sheet(is_yellow=False))
        self._layout.addWidget(self._label_strat_blue, 1, 2, 1, 3)

        label_yellow_team = QLabel('Équipe Jaune')
        label_yellow_team.setMargin(5)
        label_yellow_team.setAlignment(Qt.AlignCenter)
        label_yellow_team.setStyleSheet(self._get_style_sheet(is_yellow=True))
        self._layout.addWidget(label_yellow_team, 1, 5)

        self._label_strat_yellow = QLabel('None')
        self._label_strat_yellow.setMargin(5)
        self._label_strat_yellow.setAlignment(Qt.AlignCenter)
        self._label_strat_yellow.setStyleSheet(self._get_style_sheet(is_yellow=True))
        self._layout.addWidget(self._label_strat_yellow, 1, 6, 1, 3)

        # Sub header
        for i, header in enumerate(['Robot', 'Tactique', 'Action', 'Target']*2, start=1):
            label = QLabel(header)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(self._get_style_sheet(bold=True))
            self._layout.addWidget(label, 2, i)

        # id robot
        for i in range(6):
            for j in range(2):
                label = QLabel(str(i))
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self._get_style_sheet(bold=True))
                self._layout.addWidget(label, 3 + i, 1 + 4 * j)

        # None value everywhere else
        for i in range(6):
            for j in [1, 2, 3, 5, 6, 7]:
                label = QLabel('None')
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self._get_style_sheet(color='#222222'))
                self._layout.addWidget(label, 3 + i, 1 + j)

    def init_loop(self):
        self._logger.debug('INIT: Robot State Loop')
        self._robot_state_loop.run = self.update_robot_state
        self._robot_state_loop.daemon = True
        self._robot_state_loop.start()

        self._logger.debug('INIT: Game State Loop')
        self._game_state_loop.run = self.update_game_state
        self._game_state_loop.daemon = True
        self._game_state_loop.start()

    def update_game_state(self):
        self._logger.debug('RUN: Thread GameState')
        while True:
            game_state = self._ctrl.waiting_for_game_state()
            self._logger.debug('RUN: Received game state')
            if not self._layout.itemAtPosition(1, 6).widget().text() == str(game_state['yellow']):
                self._layout.itemAtPosition(1, 6).widget().setText(str(game_state['yellow']))
            if not self._layout.itemAtPosition(1, 2).widget().text() == str(game_state['blue']):
                self._layout.itemAtPosition(1, 2).widget().setText(str(game_state['blue']))

    def update_robot_state(self):
        self._logger.debug('RUN: Thread RobotState')
        while True:
            robot_state = self._ctrl.waiting_for_robot_state()
            self._logger.debug('RUN: Received robot state')
            if robot_state.data['team'].lower() == 'blue':
                col = 2
            else:
                col = 6
            line = 3 + robot_state.data['id']

            for i, header in enumerate(['tactic', 'action', 'target']):
                if robot_state.data[header] is not None:
                    self._logger.debug('RUN: id={} {}={}'.format(robot_state.data['id'], header, robot_state.data[header]))
                    object = self._layout.itemAtPosition(line, col + i)
                    if object is not None:
                        widget = object.widget()
                        if not widget.text() == str(robot_state.data[header]):
                            widget.setText(str(robot_state.data[header]))
                    else:
                        self._logger.warn('RUN: None type detected at {}, {}'.format(line, col+i))

    def show_hide(self):
        self._logger.debug('TRIGGER: Show/Hide')
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._ctrl.resize_window()

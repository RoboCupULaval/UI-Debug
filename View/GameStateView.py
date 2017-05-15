# Under MIT License, see LICENSE.txt

import logging
from threading import Thread
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui


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
        #self.hide()
        self._logger.debug('CONSTRUCT: ... End')

    def _get_style_sheet(self, team=None, bold=False, color='black'):
        param_sheet = ' ; '.join(['color:{}'.format(color),
                                'border-style: solid',
                                'border-color: black',
                                'border-width: 1px'])
        if team is not None:
            if team == 'yellow':
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

        self._active_team = 'blue'  # TODO (pturgeon):

        # Main header
        label_blue_team = QLabel(self._active_team+' team')
        label_blue_team.setMargin(5)
        label_blue_team.setAlignment(Qt.AlignCenter)
        label_blue_team.setStyleSheet(self._get_style_sheet(self._active_team))
        self._layout.addWidget(label_blue_team, 1, 1)

        self._label_strat_blue = QLabel('None')
        self._label_strat_blue.setMargin(5)
        self._label_strat_blue.setAlignment(Qt.AlignCenter)
        self._label_strat_blue.setStyleSheet(self._get_style_sheet(self._active_team))
        self._layout.addWidget(self._label_strat_blue, 1, 2, 1, 3)

        #label_yellow_team = QLabel('Équipe Jaune')
        #label_yellow_team.setMargin(5)
        #label_yellow_team.setAlignment(Qt.AlignCenter)
        #label_yellow_team.setStyleSheet(self._get_style_sheet(is_yellow=True))
        #self._layout.addWidget(label_yellow_team, 1, 5)

        #self._label_strat_yellow = QLabel('None')
        #self._label_strat_yellow.setMargin(5)
        #self._label_strat_yellow.setAlignment(Qt.AlignCenter)
        #self._label_strat_yellow.setStyleSheet(self._get_style_sheet(is_yellow=True))
        #self._layout.addWidget(self._label_strat_yellow, 1, 6, 1, 3)

        # Sub header
        for i, header in enumerate(['Robot', 'Tactique', 'Action', 'Target'], start=1):
            label = QLabel(header)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(self._get_style_sheet(bold=True))
            self._layout.addWidget(label, 2, i)

        self._list_active_robots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # TODO (pturgeon): Créer variable globale

        # id robot
        for i in range(len( self._list_active_robots)):
            label = QLabel(str( self._list_active_robots[i]))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(self._get_style_sheet(bold=True))
            self._layout.addWidget(label, 3 + i, 1)

        # None value everywhere else
        for i in range(len( self._list_active_robots)):
            for j in [1, 2, 3]:
                label = QLabel('None')
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self._get_style_sheet(color='#222222'))
                self._layout.addWidget(label, 3 + i, 1 + j)





        '''test'''
        '''http://www.programcreek.com/python/example/82631/PyQt5.QtWidgets.QScrollArea'''
        '''http://stackoverflow.com/questions/9624281/how-to-associate-a-horizontal-scrollbar-to-multiple-groupbox'''
        self.setWindowModality(Qt.ApplicationModal)
        self.setMaximumSize(400, 230)
        self.setMinimumSize(400, 230)
        self.resize(400, 230)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(5, 5, 390, 190))
        self.scrollArea.setWidgetResizable(True)

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setGeometry(QRect(0, 0, 390, 190))
        self.plainTextEdit.setPlainText('toto')

        self.scrolllayout = QVBoxLayout()
        self.scrollwidget = QWidget()
        self.scrollwidget.setLayout(self.scrolllayout)
        self.groupboxes = []  # Keep a reference to groupboxes for later use
        for i in range(8):  # 8 groupboxes with textedit in them
            groupbox = QGroupBox('%d' % i)
            grouplayout = QHBoxLayout()
            grouptext = QTextEdit()
            grouplayout.addWidget(grouptext)
            groupbox.setLayout(grouplayout)
            self.scrolllayout.addWidget(groupbox)
            self.groupboxes.append(groupbox)

        self.scrollArea.setWidget(self.scrollwidget)

        self.acceptButton = QPushButton(self)
        self.acceptButton.setGeometry(QRect(280, 200, 100, 25))
        self.acceptButton.setText("Ok")

        self.rejectButton = QPushButton(self)
        self.rejectButton.setGeometry(QRect(160, 200, 100, 25))
        self.rejectButton.setText("Cancel")
        '''test fini'''


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
            if game_state is not None:
                if not self._layout.itemAtPosition(1, 6).widget().text() == str(game_state['yellow']):
                    self._layout.itemAtPosition(1, 6).widget().setText(str(game_state['yellow']))
                if not self._layout.itemAtPosition(1, 2).widget().text() == str(game_state['blue']):
                    self._layout.itemAtPosition(1, 2).widget().setText(str(game_state['blue']))

    def update_robot_state(self):
        self._logger.debug('RUN: Thread RobotState')
        while True:
            robot_state = self._ctrl.waiting_for_robot_state()
            self._logger.debug('RUN: Received robot state')
            if robot_state is not None:
                #_active_team = 'blue' # TODO (pturgeon): pouvoir afficher l'équipe jaune dans le tableau
                self._list_active_robots = []
                for id in robot_state[self._active_team].keys():
                    if robot_state[self._active_team][id]['action'] is not None:
                        self._list_active_robots.append(id)
                self._list_active_robots = sorted(self._list_active_robots)
                print(self._list_active_robots)

                # pour chaque ligne
                for i in range(len(self._list_active_robots)):
                    line = 3 + i
                    id = self._list_active_robots[i]
                    for state in robot_state[self._active_team][id].keys():
                        if state == 'action':
                            col = 3
                        elif state == 'target':
                            col = 4
                        else:
                            col = 2
                        object = self._layout.itemAtPosition(line, col)
                        object.widget().setText(str(robot_state[self._active_team][id][state]))
                    object = self._layout.itemAtPosition(line, 1)
                    object.widget().setText(str(self._list_active_robots[i]))

                for line in range(i+4, 15):
                    for col in range(1, 5):
                        object = self._layout.itemAtPosition(line, col)
                        if object is not None:
                            object.widget().close()
                        else:
                            break



                '''for team in robot_state.keys():
                    if team == 'blue':
                        t_col = 2
                    else:
                        t_col = 6
                    for id in robot_state[team].keys():
                        line = 3 + id
                        for state in robot_state[team][id].keys():
                            if state == 'action':
                                col = t_col + 1
                            elif state == 'target':
                                col = t_col + 2
                            else:
                                col = t_col

                            object = self._layout.itemAtPosition(line, col)
                            if object is not None:
                                if not object.widget().text() == str(robot_state[team][id][state]):
                                    self._logger.debug(
                                        'RUN: {}.{}.{} = {} at {}, {}'.format(team, id, state, robot_state[team][id][state],
                                                                              line, col))
                                    object.widget().setText(str(robot_state[team][id][state]))
                            else:
                                self._logger.warn('RUN: NoneType detected at {}, {}'.format(line, col))'''

    def show_hide(self):
        self._logger.debug('TRIGGER: Show/Hide')
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._ctrl.resize_window()

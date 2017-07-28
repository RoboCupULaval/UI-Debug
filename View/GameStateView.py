# Under MIT License, see LICENSE.txt
import logging

import collections
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit
from PyQt5.QtCore import Qt, QRect


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
        self._robot_state_loop = QThread()
        self._robot_strategic_state_loop = QThread()
        self._game_state_loop = QThread()

        # INITIALIZATION
        self.init_logger()
        self.init_ui()
        self.init_loop()
        self.hide()
        self._logger.debug('CONSTRUCT: ... End')

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.redraw_callback)
        self.update_timer.start(300)




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
        self._list_active_robots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # TODO (pturgeon): Créer variable globale

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(0, 0, 390, 190))
        self.scrollArea.setWidgetResizable(True)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Robots", ""])
        self.treeWidget.setColumnCount(2)


        self.robots_state = {'yellow':{}, 'blue':{}}
        self.prev_robots_state = {}

        self._populate_robot_state()


        self.scrollArea.setWidget(self.treeWidget)
        self._layout.addWidget(self.scrollArea)

    def init_loop(self):
        self._logger.debug('INIT: Robot Strategic State Loop')
        self._robot_strategic_state_loop.run = self.update_robot_strategic_state
        self._robot_strategic_state_loop.daemon = True
        self._robot_strategic_state_loop.start()

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

    def update_robot_strategic_state(self):
        self._logger.debug('RUN: Thread RobotStrategicState')
        while True:
            if self._ctrl.get_team_color() != self._active_team:
                self._active_team = self._ctrl.get_team_color()

            robots_state = self._ctrl.waiting_for_robot_strategic_state()
            #print(robots_state)
            self._logger.debug('RUN: Received robot strategic state')
            if robots_state is not None:
                for team_color, robots_state_team in robots_state.items():
                    for id, robot_state in robots_state_team.items():
                        if id not in self.robots_state[team_color]:
                            self.robots_state[team_color][id] = robot_state
                            self.robots_state[team_color][id]["battery_lvl"] = 10
                        else:
                            for key, value in robot_state.items():
                                self.robots_state[team_color][id][key] = value

    def update_robot_state(self):
        self._logger.debug('RUN: Thread RobotState')
        while True:
            if self._ctrl.get_team_color() != self._active_team:
                self._active_team = self._ctrl.get_team_color()

            robot_state = self._ctrl.waiting_for_robot_state()
            self._logger.debug('RUN: Received robot state')
            if robot_state is not None:
                pass
                # for n, id in enumerate(self._list_active_robots):  # Pour chaque robot
                #     if id in robot_state[self._active_team]:
                #
                #         progressBar = self.treeWidget.itemWidget(self.groupboxes[n].child(2), 1)
                #         progressBar.setValue(robot_state[self._active_team][id]['battery_lvl'])

    def _populate_robot_state(self):

        robots_state = self.robots_state.copy()[self._active_team]

        self.treeWidget.clear()
        robots_state_sorted = collections.OrderedDict(sorted(robots_state.items()))
        for id, robot_state in robots_state_sorted.items():
            subItem = QTreeWidgetItem(self.treeWidget)
            subItem.setText(0, "Robot " + str(id))

            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0, "State")
            state = QPushButton()
            state.setStyleSheet('QPushButton {color:red;border-radius: 3px;}')
            state.setText("OFF") # TODO (pturgeon):
            state.setMaximumHeight(15)
            state.setMaximumWidth(75)
            self.treeWidget.setItemWidget(subSubItem, 1, state)

            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0, "Visible")
            subSubItem.setText(1, "True")  # TODO (pturgeon):

            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0, "Batt Level")
            pbar = QProgressBar(self)
            pbar.setValue(robot_state['battery_lvl'])
            pbar.setRange(0, 100)
            pbar.setStyleSheet('QProgressBar:horizontal { border: 1px solid gray; border-radius: 3px; background: white; '
                               'padding: 1px; text-align: right; margin-right: 37px; } QProgressBar::chunk:horizontal '
                               '{ background: red ;margin-right: 2px; /* space */ width: 10px; }')
            pbar.setMaximumHeight(13)
            pbar.setMaximumWidth(75)
            self.treeWidget.setItemWidget(subSubItem, 1, pbar)

            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Tactic")
            subSubItem.setText(1, robot_state['tactic'])
            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Action")
            subSubItem.setText(1, robot_state['action'])
            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Target")
            subSubItem.setText(1, str(robot_state['target']))
            subItem.setExpanded(True)

    def redraw_callback(self):
        self._populate_robot_state()

    def show_hide(self):
        self._logger.debug('TRIGGER: Show/Hide')
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._ctrl.resize_window()

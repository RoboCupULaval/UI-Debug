# Under MIT License, see LICENSE.txt

import logging
from threading import Thread

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit
from PyQt5.QtCore import Qt, QRect, pyqtSlot
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
        self._robot_state_loop = QThread()
        self._robot_strategic_state_loop = QThread()
        self._game_state_loop = QThread()

        # INITIALIZATION
        self.init_logger()
        self.init_ui()
        self.init_loop()
        self.hide()
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
        self._list_active_robots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # TODO (pturgeon): Créer variable globale

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(0, 0, 390, 190))
        self.scrollArea.setWidgetResizable(True)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Robots", ""])
        self.treeWidget.setColumnCount(2)
        #self.setMaximumWidth(250)

        #self.batt = QtGui.QProgressBar(self)
        #self.batt.setValue(1)

        self.groupboxes = []
        for id in self._list_active_robots:
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
            pbar.setValue(10)# TODO (pturgeon):
            pbar.setRange(0, 100)
            pbar.setStyleSheet('QProgressBar:horizontal { border: 1px solid gray; border-radius: 3px; background: white; '
                               'padding: 1px; text-align: right; margin-right: 37px; } QProgressBar::chunk:horizontal '
                               '{ background: red ;margin-right: 2px; /* space */ width: 10px; }')
            pbar.setMaximumHeight(13)
            pbar.setMaximumWidth(75)
            self.treeWidget.setItemWidget(subSubItem, 1, pbar)

            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Tactic")
            for n in range(10):
                subSubSubItem = QTreeWidgetItem(subSubItem)
                subSubSubItem.setText(1, "Dummy tactic")
            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Action")
            subSubItem = QTreeWidgetItem(subItem)
            subSubItem.setText(0,"Target")
            if id < 6:
                subItem.setExpanded(True)
            self.groupboxes.append(subItem)

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

            robot_state = self._ctrl.waiting_for_robot_strategic_state()
            self._logger.debug('RUN: Received robot strategic state')
            if robot_state is not None:
                for n, id in enumerate(self._list_active_robots): # Pour chaque robot
                    if id in robot_state[self._active_team]:
                        if 'tactic' in robot_state[self._active_team][id]:
                            self.groupboxes[n].child(3).setText(1, str(robot_state[self._active_team][id]['tactic']))
                            self.groupboxes[n].child(3).child(0).setText(1, str(robot_state[self._active_team][id]['tactic']))
                            self.groupboxes[n].child(4).setText(1, str(robot_state[self._active_team][id]['action']))
                            self.groupboxes[n].child(5).setText(1, str(robot_state[self._active_team][id]['target']))

    def update_robot_state(self):
        self._logger.debug('RUN: Thread RobotState')
        while True:
            if self._ctrl.get_team_color() != self._active_team:
                self._active_team = self._ctrl.get_team_color()

            robot_state = self._ctrl.waiting_for_robot_state()
            self._logger.debug('RUN: Received robot state')
            if robot_state is not None:
                for n, id in enumerate(self._list_active_robots):  # Pour chaque robot
                    if id in robot_state[self._active_team]:

                        progressBar = self.treeWidget.itemWidget(self.groupboxes[n].child(2), 1)
                        progressBar.setValue(robot_state[self._active_team][id]['battery_lvl'])


    def show_hide(self):
        self._logger.debug('TRIGGER: Show/Hide')
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._ctrl.resize_window()

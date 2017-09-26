# Under MIT License, see LICENSE.txt
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QComboBox, \
                            QPushButton, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal

__author__ = 'RoboCupULaval'


class StrategyCtrView(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.play_info = None
        # self.play_info = {'referee_info': 'Unknown',
        #                   'referee_team_info': 'Unknown',
        #                   'auto_play_info': 'Unknown',
        #                   'referee': {'command': '',
        #                               'stage': '',
        #                               'stage_time_left': -597707000},
        #                   'referee_team': {'ours': {'name': '',
        #                                             'score': 0,
        #                                             'red_cards': 0,
        #                                             'yellow_cards': 0,
        #                                             'yellow_card_times': [],
        #                                             'timeouts': 0,
        #                                             'timeout_time': 300000000,
        #                                             'goalie': 0},
        #                                    'theirs': {'name': '',
        #                                               'score': 0,
        #                                               'red_cards': 0,
        #                                               'yellow_cards': 0,
        #                                               'yellow_card_times': [],
        #                                               'timeouts': 0,
        #                                               'timeout_time': 300000000,
        #                                               'goalie': 0}},
        #                   'auto_play': {'selected_strategy': '',
        #                                 'current_state': ''},
        #                   'auto_flag': False}

        self.init_ui()
        self.hide()

        self._play_info_loop = QThread()
        self.init_loop()

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_combobox)
        self.update_timer.start(500)

    def init_loop(self):
        self._play_info_loop.run = self.update_play_info
        self._play_info_loop.daemon = True
        self._play_info_loop.start()

    def init_ui(self):
        self._active_team = 'green'

        # Création des pages d'onglet
        self.main_layout = QVBoxLayout(self)
        self.page_controller = QTabWidget(self)
        self.page_autonomous = QWidget()
        self.page_strategy = QWidget()
        self.page_tactic = QWidget()
        self.main_layout.addWidget(self.page_controller)
        self._layout = self.main_layout

        # Création du contenu des pages
        # + Page Team
        self.page_autonomous_vbox = QVBoxLayout()
        self.page_autonomous_scrollarea = QScrollArea(self)
        self.page_autonomous_scrollarea.setGeometry(QRect(0, 0, 390, 190))
        self.page_autonomous_scrollarea.setWidgetResizable(True)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["", ""])
        self.treeWidget.setColumnCount(2)
        self.page_autonomous_scrollarea.setWidget(self.treeWidget)

        self._populate_play_info()


        self.page_autonomous_but_play = QPushButton("Start")
        self.page_autonomous_but_play.clicked.connect(self.send_start_auto)
        but_play_font = QFont()
        but_play_font.setBold(True)
        self.page_autonomous_but_play.setFont(but_play_font)
        self.page_autonomous_but_play.setStyleSheet('QPushButton {color:green;}')

        self.page_autonomous_but_stop = QPushButton("Stop")
        self.page_autonomous_but_stop.clicked.connect(self.send_stop_auto)
        self.page_autonomous_but_stop.setFont(but_play_font)
        self.page_autonomous_but_stop.setStyleSheet('QPushButton {color:red;}')
        self.page_autonomous_but_stop.setVisible(False)

        self.page_autonomous_vbox.addWidget(self.page_autonomous_scrollarea)
        self.page_autonomous_vbox.addWidget(self.page_autonomous_but_play)
        self.page_autonomous_vbox.addWidget(self.page_autonomous_but_stop)

        self.page_autonomous.setLayout(self.page_autonomous_vbox)

        # + Page Strategy
        self.page_strat_vbox = QVBoxLayout()
        self.selectStrat = QComboBox()
        self.selectStrat.addItem('Aucune Stratégie disponible')

        self.page_strat_but_apply = QPushButton('Appliquer')
        self.page_strat_but_apply.clicked.connect(self.send_strat)
        self.page_strat_but_cancel = QPushButton("STOP")
        but_cancel_font = QFont()
        but_cancel_font.setBold(True)
        self.page_strat_but_cancel.setFont(but_cancel_font)
        self.page_strat_but_cancel.setStyleSheet('QPushButton {color:red;}')
        self.page_strat_but_cancel.clicked.connect(self.send_strat_stop)

        qgroup = QGroupBox('Sélectionnez votre stratégie', self.page_strategy)
        strat_combox = QVBoxLayout()
        strat_combox.addWidget(self.selectStrat)
        qgroup.setLayout(strat_combox)

        but_group = QHBoxLayout()
        but_group.addWidget(self.page_strat_but_apply)
        but_group.addWidget(self.page_strat_but_cancel)
        self.page_strat_vbox.addWidget(qgroup)
        self.page_strat_vbox.addLayout(but_group)

        self.page_strategy.setLayout(self.page_strat_vbox)

        # + Page Tactic
        self.page_tact_vbox = QVBoxLayout()

        group_bot_select = QGroupBox('Sélectionnez la tactique du robot', self.page_tactic)
        group_vbox = QVBoxLayout()
        group_bot_select.setLayout(group_vbox)

        group_vbox.addWidget(QLabel('ID du robot :'))
        self.selectRobot = QComboBox()
        [self.selectRobot.addItem(str(x)) for x in range(12)]
        self.selectRobot.currentIndexChanged.connect(self.handle_selection_robot_event_id)
        group_vbox.addWidget(self.selectRobot)

        group_vbox.addWidget(QLabel('Tactique à appliquer :'))
        self.selectTactic = QComboBox()
        self.selectTactic.addItem('Aucune Tactique disponible')
        group_vbox.addWidget(self.selectTactic)
        self.argumentsLine = QLineEdit()
        group_vbox.addWidget(self.argumentsLine)

        but_group_tact = QHBoxLayout()
        tact_apply_but = QPushButton('Appliquer')
        tact_apply_but.clicked.connect(self.send_tactic)
        but_group_tact.addWidget(tact_apply_but)

        tact_stop_but = QPushButton('STOP')
        tact_stop_but.setFont(but_cancel_font)
        tact_stop_but.setStyleSheet('QPushButton {color:red;}')
        tact_stop_but.clicked.connect(self.send_tactic_stop)
        but_group_tact.addWidget(tact_stop_but)

        tact_stop_all_but = QPushButton('STOP ALL')
        tact_stop_all_but.setFont(but_cancel_font)
        tact_stop_all_but.setStyleSheet('QPushButton {color:red;}')
        tact_stop_all_but.clicked.connect(self.send_tactic_stop_all)

        self.page_tact_vbox.addWidget(group_bot_select)
        self.page_tact_vbox.addLayout(but_group_tact)
        self.page_tact_vbox.addWidget(tact_stop_all_but)

        self.page_tactic.setLayout(self.page_tact_vbox)

        # + Onglets
        self.page_controller.addTab(self.page_autonomous, 'AutoPlay')
        self.page_controller.addTab(self.page_strategy, 'Stratégie')
        self.page_controller.addTab(self.page_tactic, 'Tactique')
        self.page_controller.currentChanged.connect(self.tab_selected)

    @pyqtSlot(int)
    def handle_selection_robot_event_id(self, index):
        self.parent.deselect_all_robots()
        self.parent.select_robot(index, self.parent.get_team_color())

    @pyqtSlot(int)
    def handle_selection_robot_event_team(self, index):
        self.parent.deselect_all_robots()
        self.parent.select_robot(self.selectRobot.currentIndex(), self.parent.get_team_color())

    @pyqtSlot(int)
    def tab_selected(self, index):
        if index == 0 or index == 1:
            self.parent.deselect_all_robots()
        elif index == 2:
            id_bot = self.selectRobot.currentIndex()
            self.parent.select_robot(id_bot, self.parent.get_team_color())

    @pyqtSlot(str)
    def handle_team_color(self, team_color):
        self._active_team = team_color.lower()
        self.teamColorLabel.setText(self.parent.get_team_color().capitalize())

    def hideEvent(self, event):
        self.parent.deselect_all_robots()
        super().hideEvent(event)

    def update_combobox(self):
        if self.parent.model_datain._data_STA_config is not None:
            data = self.parent.model_datain._data_STA_config.data

            if data['tactic'] is not None:
                tactics = self.get_tactic_list()
                for tact in data['tactic']:
                    if not tact in tactics:
                        self.refresh_tactic(data['tactic'])
                        break

            if data['strategy'] is not None:
                strats = self.get_strat_list()
                for strat in data['strategy']:
                    if not strat in strats:
                        self.refresh_strat(data['strategy'])
                        break
        self._populate_play_info()

    def get_strat_list(self):
        strat = []
        for i in range(self.selectStrat.count()):
            if not self.selectStrat.count() == 1:
                strat.append(self.selectStrat.itemText(i))
        return strat

    def get_tactic_list(self):
        tactics = []
        for i in range(self.selectTactic.count()):
            if not self.selectTactic.count() == 1:
                tactics.append(self.selectTactic.itemText(i))
        return tactics

    def refresh_tactic(self, tactics):
        self.selectTactic.clear()
        if tactics is not None:
            for tactic in tactics:
                self.selectTactic.addItem(tactic)
        else:
            self.selectTactic.addItem('Aucune Tactique disponible')

    def refresh_strat(self, strats):
        self.selectStrat.clear()
        if strats is not None:
            for strat in strats:
                self.selectStrat.addItem(strat)
        else:
            self.selectStrat.addItem('Aucune Stratégie disponible')

    def send_strat(self):
        strat = str(self.selectStrat.currentText())
        if not strat == 'Aucune Stratégie disponible':
            self.parent.model_dataout.send_strategy(strat, self.parent.get_team_color())

    def send_tactic(self):
        id_bot = int(self.selectRobot.currentText())
        tactic = str(self.selectTactic.currentText())
        args = str(self.argumentsLine.text()).split()
        target = self.parent.model_dataout.target
        if not tactic == 'Aucune Tactique disponible':
            self.parent.model_dataout.send_tactic(id_bot, self.parent.get_team_color(), tactic=tactic, target=target, args=args)

    def send_tactic_stop(self):
        id_bot = int(self.selectRobot.currentText())
        self.parent.model_dataout.send_tactic(id_bot, self.parent.get_team_color(), 'tStop', args=None)

    def send_tactic_stop_all(self):
        for id_bot in range(12):  # TODO (pturgeon): Changer pour constante globable (ou liste?)
            self.parent.model_dataout.send_tactic(id_bot, self.parent.get_team_color(), 'tStop', args=None)

    def send_strat_stop(self):
        self.parent.model_dataout.send_strategy('pStop', self.parent.get_team_color())

    def toggle_show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.parent.resize_window()

    def send_start_auto(self):
        self.parent.model_dataout.send_auto_play(True)

    def send_stop_auto(self):
        self.parent.model_dataout.send_auto_play(False)
        
    def _populate_play_info(self):
        self.treeWidget.clear()

        if self.play_info is None:
            return

        self.teamColorRow = QTreeWidgetItem(self.treeWidget)
        self.teamColorRow.setText(0, "Our color")
        self.teamColorRow.setText(1, self.parent.get_team_color().capitalize())

        self.refereeInfo = QTreeWidgetItem(self.treeWidget)
        self.refereeInfo.setText(0, "Referee info")
        self.refereeInfo.setExpanded(True)
        self.currentRefCommand = QTreeWidgetItem(self.refereeInfo)
        self.currentRefCommand.setText(0, "Command")
        self.currentRefCommand.setText(1, self.play_info['referee']['command'])

        self.currentGameStage = QTreeWidgetItem(self.refereeInfo)
        self.currentGameStage.setText(0, "Stage")
        self.currentGameStage.setText(1, self.play_info['referee']['stage'])

        self.stageTimeLeftItem = QTreeWidgetItem(self.refereeInfo)
        self.stageTimeLeftItem.setText(0, "Stage time left")
        self.stageTimeLeft = QTimeEdit(QTime().fromMSecsSinceStartOfDay(self.play_info['referee']['stage_time_left'] / 1000))
        self.stageTimeLeft.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.stageTimeLeft.setReadOnly(True)
        self.stageTimeLeft.setDisplayFormat("m:ss")
        self.treeWidget.setItemWidget(self.stageTimeLeftItem, 1, self.stageTimeLeft)

        
        self.autoPlayInfo = QTreeWidgetItem(self.treeWidget)
        self.autoPlayInfo.setText(0, "AutoPlay info")
        self.autoPlayInfo.setExpanded(True)
        self.autoState = QTreeWidgetItem(self.autoPlayInfo)
        self.autoState.setText(0, "State")
        self.autoState.setText(1, self.play_info['auto_play']['current_state'])

        self.currentStrategy = QTreeWidgetItem(self.autoPlayInfo)
        self.currentStrategy.setText(0, "Strategy")
        self.currentStrategy.setText(1, self.play_info['auto_play']['selected_strategy'])


        self.teamInfo = {}
        for team in ("ours", "theirs"):
            info = self.play_info["referee_team"][team]
            self.teamInfo[team] = {}
            self.teamInfo[team]["item"] = QTreeWidgetItem(self.treeWidget)
            self.teamInfo[team]["item"].setText(0, info["name"])
            self.teamInfo[team]["goalie"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["goalie"].setText(0, "Goalie ID")
            self.teamInfo[team]["goalie"].setText(1, str(info["goalie"]))
            self.teamInfo[team]["score"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["score"].setText(0, "Score")
            self.teamInfo[team]["score"].setText(1,str(info["score"]))
            self.teamInfo[team]["red_cards"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["red_cards"].setText(0, "Red cards")
            self.teamInfo[team]["red_cards"].setText(1, str(info["red_cards"]))
            self.teamInfo[team]["yellow_cards"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["yellow_cards"].setText(0, "Yellow cards")
            self.teamInfo[team]["yellow_cards"].setText(1, str(info["yellow_cards"]))
            self.teamInfo[team]["yellow_card_times_item"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["yellow_card_times_item"].setText(0, "Yellow cards time")
            if len(info["yellow_card_times"]):
                yellow_card_time = min(info["yellow_card_times"]) / 1000
            else:
                yellow_card_time = 0
            self.teamInfo[team]["yellow_card_times"] = QTimeEdit(QTime().fromMSecsSinceStartOfDay(yellow_card_time))
            self.teamInfo[team]["yellow_card_times"].setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.teamInfo[team]["yellow_card_times"].setReadOnly(True)
            self.teamInfo[team]["yellow_card_times"].setDisplayFormat("m:ss")
            self.treeWidget.setItemWidget(self.teamInfo[team]["yellow_card_times_item"], 1,
                                          self.teamInfo[team]["yellow_card_times"])
            self.teamInfo[team]["timeouts"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["timeouts"].setText(0, "Timeouts")
            self.teamInfo[team]["timeouts"].setText(1, str(info["timeouts"]))
            self.teamInfo[team]["timeout_time_item"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["timeout_time_item"].setText(0, "Timeout time")
            self.teamInfo[team]["timeout_time"] = QTimeEdit(QTime().fromMSecsSinceStartOfDay(info["timeout_time"] / 1000))
            self.teamInfo[team]["timeout_time"].setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.teamInfo[team]["timeout_time"].setReadOnly(True)
            self.teamInfo[team]["timeout_time"].setDisplayFormat("m:ss")
            self.treeWidget.setItemWidget(self.teamInfo[team]["timeout_time_item"], 1,
                                          self.teamInfo[team]["timeout_time"])
            self.teamInfo[team]["item"].setExpanded(True)

        if self.parent.get_team_color() != self._active_team:
            self._active_team = self.parent.get_team_color()
            self.teamColorRow.setText(1, self._active_team.capitalize())

        

    def update_play_info(self):
        while True:

            self.play_info = self.parent.waiting_for_play_info()

            self.page_autonomous_but_stop.setVisible(self.play_info['auto_flag'])
            self.page_autonomous_but_play.setVisible(not self.play_info['auto_flag'])




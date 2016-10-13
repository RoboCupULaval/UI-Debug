# Under MIT License, see LICENSE.txt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *

__author__ = 'RoboCupULaval'


class StrategyCtrView(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.hide()

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_combobox)
        self.update_timer.start(500)

    def init_ui(self):
        self.setFixedWidth(300)
        # Création des pages d'onglet
        self.page_controller = QTabWidget(self)
        self.page_strategy = QWidget()
        self.page_tactic = QWidget()

        # Création du contenu des pages
        # + Page Strategy
        self.page_strat_vbox = QVBoxLayout()
        self.selectStrat = QComboBox()
        self.selectStrat.addItem('Aucune Stratégie disponible')

        self.selectStratTeam = QComboBox()
        self.selectStratTeam.addItem('Yellow')
        self.selectStratTeam.addItem('Blue')

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
        strat_combox.addWidget(self.selectStratTeam)
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
        [self.selectRobot.addItem(str(x)) for x in range(6)]
        group_vbox.addWidget(self.selectRobot)

        group_vbox.addWidget(QLabel('Équipe :'))
        self.selectTeam = QComboBox()
        self.selectTeam.addItem('Yellow')
        self.selectTeam.addItem('Blue')
        group_vbox.addWidget(self.selectTeam)

        group_vbox.addWidget(QLabel('Tactique à appliquer :'))
        self.selectTactic = QComboBox()
        self.selectTactic.addItem('Aucune Tactique disponible')
        group_vbox.addWidget(self.selectTactic)

        but_group_tact = QHBoxLayout()
        tact_apply_but = QPushButton('Appliquer')
        tact_apply_but.clicked.connect(self.send_tactic)
        but_group_tact.addWidget(tact_apply_but)

        tact_stop_but = QPushButton('STOP')
        tact_stop_but.setFont(but_cancel_font)
        tact_stop_but.setStyleSheet('QPushButton {color:red;}')
        tact_stop_but.clicked.connect(self.send_tactic_stop)
        but_group_tact.addWidget(tact_stop_but)

        self.page_tact_vbox.addWidget(group_bot_select)
        self.page_tact_vbox.addLayout(but_group_tact)

        self.page_tactic.setLayout(self.page_tact_vbox)

        # + Onglets
        self.page_controller.addTab(self.page_strategy, 'Stratégie')
        self.page_controller.addTab(self.page_tactic, 'Tactique')

        # SIGNAL / SLOT
        self.connect(self.page_controller, SIGNAL('currentChanged(int)'),
                     self, SLOT('tab_selected(int)'))
        self.connect(self.selectRobot, SIGNAL('currentIndexChanged(int)'),
                     self, SLOT('handle_selection_robot_event_id(int)'))
        self.connect(self.selectTeam, SIGNAL('currentIndexChanged(int)'),
                     self, SLOT('handle_selection_robot_event_team(int)'))

    @pyqtSlot(int)
    def handle_selection_robot_event_id(self, index):
        self.parent.deselect_all_robots()
        self.parent.select_robot(index, True if self.selectTeam.currentText() == 'Yellow' else False)

    @pyqtSlot(int)
    def handle_selection_robot_event_team(self, index):
        self.parent.deselect_all_robots()
        self.parent.select_robot(self.selectRobot.currentIndex(), True if index == 0 else False)

    @pyqtSlot(int)
    def tab_selected(self, index):
        if index == 0:
            self.parent.deselect_all_robots()
        elif index == 1:
            id_bot = self.selectRobot.currentIndex()
            self.parent.select_robot(id_bot, True if self.selectTeam.currentText() == 'Yellow' else False)

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
        team = str(self.selectStratTeam.currentText()).lower()
        if not strat == 'Aucune Stratégie disponible':
            self.parent.model_dataout.send_strategy(strat, team)

    def send_tactic(self):
        id_bot = int(self.selectRobot.currentText())
        is_yellow = True if self.selectTeam == 'Yellow' else False
        if not is_yellow:
            id_bot += 6
        tactic = str(self.selectTactic.currentText())
        target = self.parent.model_dataout.target
        if not tactic == 'Aucune Tactique disponible':
            self.parent.model_dataout.send_tactic(id_bot, tactic, target)

    def send_tactic_stop(self):
        for id_bot in range(6):
            self.parent.model_dataout.send_tactic(id_bot, 'tStop')

    def send_strat_stop(self):
        self.parent.model_dataout.send_strategy('pStop', 'yellow')
        self.parent.model_dataout.send_strategy('pStop', 'blue')

    def toggle_show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.parent.resize_window()
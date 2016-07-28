# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import *
from PyQt4.QtCore import *

__author__ = 'RoboCupULaval'


class StrategyCtrView(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.hide()

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
        group_vbox.addWidget(self.selectRobot)
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

        # + Onglet
        self.page_controller.addTab(self.page_strategy, 'Stratégie')
        self.page_controller.addTab(self.page_tactic, 'Tactique')

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
            self.parent.model_dataout.send_strategy(strat)

    def send_tactic(self):
        id_bot = str(self.selectRobot.currentText())
        tactic = str(self.selectTactic.currentText())
        target = str(self.parent.model_dataout.target)
        if not tactic == 'Aucune Tactique disponible':
            self.parent.model_dataout.send_tactic(id_bot, tactic, target)

    def send_tactic_stop(self):
        for id_bot in range(6):
            self.parent.model_dataout.send_tactic(id_bot, 'tStop')

    def send_strat_stop(self):
        self.parent.model_dataout.send_strategy('pStop')

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.parent.resize_window()
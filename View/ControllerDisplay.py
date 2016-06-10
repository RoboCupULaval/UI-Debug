# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import *

__author__ = 'RoboCupULaval'


class ControllerDisplay(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setFixedSize(300, 700)
        self.init_ui()
        self.hide()

    def init_ui(self):
        # Configuration des Label
        self.title = QLabel('Tactic Controller', self)
        font = QFont()
        font.setBold(True)
        font.setPixelSize(20)
        self.title.setFont(font)
        self.robot = QLabel('Robot: ', self)
        self.robot.move(0, 50)
        self.tactic = QLabel('Tactique: ', self)
        self.tactic.move(0, 100)

        # Configuration des ComboBox
        self.selectRobot = QComboBox(self)
        for x in range(6+6):
            self.selectRobot.addItem(str(x))
        self.selectRobot.move(50, 50)

        self.selectTactic = QComboBox(self)
        self.selectTactic.move(50, 100)
        self.refresh_tactic()

        # Configuration des PushButton
        self.btn_apply = QPushButton('Appliquer', self)
        self.btn_apply.clicked.connect(self.send_tactic)
        self.btn_apply.move(0, 150)

        self.btn_refresh = QPushButton('Rafraîchir', self)
        self.btn_refresh.clicked.connect(self.refresh_tactic)
        self.btn_refresh.move(100, 150)

        self.btn_stop = QPushButton('STOP', self)
        self.btn_stop.clicked.connect(self.send_tactic_stop)
        self.btn_stop.move(200, 150)

    def refresh_tactic(self):
        self.selectTactic.clear()
        tactics = self.parent.datain_model.get_tactics()
        if tactics is not None:
            for tactic in tactics:
                self.selectTactic.addItem(tactic)
        else:
            self.selectTactic.addItem('Aucune disponible')

    def send_tactic(self):
        id_bot = str(self.selectRobot.currentText())
        tactic = str(self.selectTactic.currentText())
        target = str(self.parent.dataout_model.target)
        if not tactic == 'Aucune disponible':
            self.parent.dataout_model.send_tactic(id_bot, tactic, target)

    def send_tactic_stop(self):
        for id_bot in range(6):
            self.parent.dataout_model.send_tactic(id_bot, 'tStop')

    def show_hide(self):
        if self.isVisible():
            self.hide()
            self.parent.setFixedSize(1025, 750)
        else:
            self.parent.setFixedSize(1325, 750)
            self.show()

# Under MIT License, see LICENSE.txt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QComboBox, \
                            QPushButton, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal

__author__ = 'RoboCupULaval'


class GrsimCtrView(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(300)
        self.setFixedHeight(150)
        self.teams = QHBoxLayout()
        # blue team
        self.qBlueGrouproup = QGroupBox('Blue Team', self)
        blueTeamLayout = QVBoxLayout()
        self.qResetBlue1 = QPushButton("Reset", self.qBlueGrouproup)
        self.qResetBlue1.clicked.connect(self.send_command)

        blueTeamLayout.addWidget(self.qResetBlue1)
        self.qBlueGrouproup.setLayout(blueTeamLayout)

        # yellow team
        self.qYellowGrouproup = QGroupBox('Yellow Team', self)
        yellowTeamLayout = QVBoxLayout()

        self.qResetYellow1 = QPushButton("Reset", self.qYellowGrouproup)
        self.qResetYellow1.clicked.connect(self.send_command)

        yellowTeamLayout.addWidget(self.qResetYellow1)
        self.qYellowGrouproup.setLayout(yellowTeamLayout)

        self.teams.addWidget(self.qBlueGrouproup)
        self.teams.addWidget(self.qYellowGrouproup)
        self.setLayout(self.teams)
        self.setHidden(False)
        pass

    def send_command(self):
        print("sdfasdfsdf")


    def toggle_show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.parent.resize_window()
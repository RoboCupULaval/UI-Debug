# Under MIT License, see LICENSE.txt

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL

from Model.FrameModel import FrameModel
from View.FieldDisplay import FieldDisplay

__author__ = 'RoboCupULaval'


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('RoboCup ULaval | GUI Debug')
        self.layout = QHBoxLayout()
        self.model = FrameModel()

        self.view_property = QTableView()
        # self.view_property.setModel(self.model)

        self.view_screen = FieldDisplay()
        self.view_screen.set_model(self.model)

        self.layout.addWidget(self.view_screen)
        self.layout.addWidget(self.view_property)
        self.setLayout(self.layout)

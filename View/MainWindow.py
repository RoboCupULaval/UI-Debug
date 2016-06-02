# Under MIT License, see LICENSE.txt

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL

from Model.FrameModel import FrameModel
from View.FieldDisplay import FieldDisplay

__author__ = 'RoboCupULaval'


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('RoboCup ULaval | GUI Debug')
        self.setWindowIcon(QIcon('Img/favicon.jpg'))
        self.menubar = QMenuBar(self)
        self.layout = QVBoxLayout()
        self.model = FrameModel()

        self.view_property = QTableView()
        # self.view_property.setModel(self.model)

        self.view_screen = FieldDisplay()
        self.view_screen.set_model(self.model)

        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.view_screen)
        self.layout.addWidget(self.view_property)
        self.setLayout(self.layout)

        self.init_menubar()
        self.init_signals()

    def init_menubar(self):
        # Menu
        fileMenu = self.menubar.addMenu('Fichier')
        viewMenu = self.menubar.addMenu('Vue')
        helpMenu = self.menubar.addMenu('Aide')

        # Sous-menu
        exitAction = QAction('Quitter', self)
        exitAction.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitAction)

        vanishAction = QAction('Afficher Vanishing', self, checkable=True)
        vanishAction.triggered.connect(self.view_screen.change_vanish_option)
        viewMenu.addAction(vanishAction)

    def init_signals(self):
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    def closeEvent(self, event):
        self.close()

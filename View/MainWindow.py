# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL

from Model.FrameModel import FrameModel
from Model.DataInModel import DataInModel
from Model.DataOutModel import DataOutModel
from .FieldView import FieldView
from .StrategyCtrView import StrategyCtrView

__author__ = 'RoboCupULaval'


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('RoboCup ULaval | GUI Debug')
        self.setWindowIcon(QIcon('Img/favicon.jpg'))
        self.setFixedSize(1025, 750)
        self.menubar = QMenuBar(self)
        self.layout = QVBoxLayout()
        self.sub_layout = QHBoxLayout()
        self.frame_model = FrameModel()
        self.datain_model = DataInModel()
        self.dataout_model = DataOutModel()

        self.view_controller = StrategyCtrView(self)
        # self.view_property.setModel(self.model)

        self.view_screen = FieldView(self)
        self.view_screen.set_model(self.frame_model)

        self.layout.addWidget(self.menubar)
        self.sub_layout.addWidget(self.view_screen)
        self.sub_layout.addWidget(self.view_controller)
        self.layout.addLayout(self.sub_layout)
        self.setLayout(self.layout)

        self.init_menubar()
        self.init_signals()

    def init_menubar(self):
        # Menu
        fileMenu = self.menubar.addMenu('Fichier')
        viewMenu = self.menubar.addMenu('Vue')
        toolMenu = self.menubar.addMenu('Outil')
        helpMenu = self.menubar.addMenu('Aide')

        # Sous-menu
        helpAction = QAction('À propos', self)
        helpAction.triggered.connect(self.credits)
        helpMenu.addAction(helpAction)

        exitAction = QAction('Quitter', self)
        exitAction.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitAction)

        vanishAction = QAction('Afficher Vanishing', self, checkable=True)
        vanishAction.triggered.connect(self.view_screen.change_vanish_option)
        viewMenu.addAction(vanishAction)

        nuumbAction = QAction('Afficher Numéro des robots', self, checkable=True)
        nuumbAction.triggered.connect(self.view_screen.show_number_option)
        viewMenu.addAction(nuumbAction)

        tacticsControllerAction = QAction('Contrôleur de Stratégie', self,  checkable=True)
        tacticsControllerAction.triggered.connect(self.view_controller.show_hide)
        toolMenu.addAction(tacticsControllerAction)

    def init_signals(self):
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    def credits(self):
        QMessageBox.about(self, 'À Propos', 'ROBOCUP ULAVAL © 2016\n\ncontact@robocupulaval.com')

    def closeEvent(self, event):
        self.close()

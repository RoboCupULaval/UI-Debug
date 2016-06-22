# Under MIT License, see LICENSE.txt

from time import sleep

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL

from Model.FrameModel import FrameModel
from Model.DataInModel import DataInModel
from Model.DataOutModel import DataOutModel

from View.FieldView import FieldView
from View.StrategyCtrView import StrategyCtrView
from View.LoggerView import LoggerView
from View.MainWindow import MainWindow

from .DrawController import DrawController
from .FieldController import FieldController

__author__ = 'RoboCupULaval'


class MainController(QWidget):
    # TODO: Dissocier Controller de la fenêtre principale
    def __init__(self):
        QWidget.__init__(self)

        # Création des Modèles
        self.model_frame = FrameModel(self)
        self.model_datain = DataInModel(self)
        self.model_dataout = DataOutModel(self)

        # Création des Vues
        self.main_window = MainWindow()
        self.view_menu = QMenuBar(self)
        self.view_logger = LoggerView(self)
        self.view_controller = StrategyCtrView(self)
        self.view_screen = FieldView(self)

        # Création des Contrôleurs
        self.draw_handler = DrawController()
        self.field_handler = FieldController()

        # Initialisation des UI
        self.init_main_window()
        self.init_menubar()
        self.init_signals()
        self.resize_window()

    def init_main_window(self):
        # Initialisation de la fenêtre
        self.setWindowTitle('RoboCup ULaval | GUI Debug')
        self.setWindowIcon(QIcon('Img/favicon.jpg'))

        # Initialisation des Layouts
        # => Field | StratController (Horizontal)
        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.view_screen)
        sub_layout.addWidget(self.view_controller)

        # => Menu | SubLayout | Logger (Vertical)
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.view_menu)
        top_layout.addLayout(sub_layout)
        top_layout.addWidget(self.view_logger)

        self.setLayout(top_layout)

        # Initialisation des modèles aux vues
        self.view_logger.set_model(self.model_datain)
        self.view_screen.set_model(self.model_frame)

    def init_menubar(self):
        # Titre des menus et dimension
        self.view_menu.setFixedHeight(30)
        fileMenu = self.view_menu.addMenu('Fichier')
        viewMenu = self.view_menu.addMenu('Vue')
        toolMenu = self.view_menu.addMenu('Outil')
        helpMenu = self.view_menu.addMenu('Aide')

        # Action et entête des sous-menus
        # => Menu Aide
        helpAction = QAction('À propos', self)
        helpAction.triggered.connect(self.aboutMsgBox)
        helpMenu.addAction(helpAction)

        # => Menu Fichier
        exitAction = QAction('Quitter', self)
        exitAction.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitAction)

        # => Menu Vue
        vanishAction = QAction('Afficher Vanishing', self, checkable=True)
        vanishAction.triggered.connect(self.view_screen.change_vanish_option)
        viewMenu.addAction(vanishAction)

        nuumbAction = QAction('Afficher Numéro des robots', self, checkable=True)
        nuumbAction.triggered.connect(self.view_screen.show_number_option)
        viewMenu.addAction(nuumbAction)

        # => Menu Outil
        StrategyControllerAction = QAction('Contrôleur de Stratégie', self,  checkable=True)
        StrategyControllerAction.triggered.connect(self.view_controller.show_hide)
        toolMenu.addAction(StrategyControllerAction)

        loggerAction = QAction('Afficher le Logger', self,  checkable=True)
        loggerAction.triggered.connect(self.view_logger.show_hide)
        toolMenu.addAction(loggerAction)

    def init_signals(self):
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    def update_logging(self):
        self.view_logger.refresh()

    def save_logging(self, path):
        self.model_datain.save_logging(path)

    def aboutMsgBox(self):
        QMessageBox.about(self, 'À Propos', 'ROBOCUP ULAVAL © 2016\n\ncontact@robocupulaval.com')

    def closeEvent(self, event):
        self.close()

    def resize_window(self):
        self.setFixedSize(self.minimumSizeHint())

    def show_draw(self, draw):
        try:
            for key, item in draw.data.items():
                if isinstance(item, tuple) and len(item) == 2:
                    x, y, _ = self.field_handler.convert_real_to_scene_pst(item[0], item[1])
                    draw.data[key] = x, y
            qt_draw = self.draw_handler.get_qt_draw_object(draw)
            self.view_screen.load_draw(qt_draw)
        except NotImplemented():
            print('@qt_draw not implemented yet.')

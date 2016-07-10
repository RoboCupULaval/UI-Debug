# Under MIT License, see LICENSE.txt

from signal import signal, SIGINT

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from Model.FrameModel import FrameModel
from Model.DataInModel import DataInModel
from Model.DataOutModel import DataOutModel

from View.FieldView import FieldView
from View.StrategyCtrView import StrategyCtrView
from View.LoggerView import LoggerView
from View.MainWindow import MainWindow

from .QtObjectFactory import QtObjectFactory
from .FieldController import FieldController

__author__ = 'RoboCupULaval'


class MainController(QWidget):
    # TODO: Dissocier Controller de la fenêtre principale
    def __init__(self):
        QWidget.__init__(self)

        # Création des Contrôleurs
        self.draw_handler = QtObjectFactory(self)

        # Création des Vues
        self.main_window = MainWindow()
        self.view_menu = QMenuBar(self)
        self.view_logger = LoggerView(self)
        self.view_controller = StrategyCtrView(self)
        self.view_screen = FieldView(self)

        # Création des Modèles
        self.model_frame = FrameModel(self)
        self.model_datain = DataInModel(self)
        self.model_dataout = DataOutModel(self)

        # Initialisation des UI
        self.init_main_window()
        self.init_menubar()
        self.init_signals()
        self.resize_window()

    def init_main_window(self):
        # Initialisation de la fenêtre
        self.setWindowTitle('RoboCup ULaval | GUI Debug')
        self.setWindowIcon(QIcon('Img/favicon.jpg'))
        self.resize(975, 750)

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

    def init_menubar(self):
        # Titre des menus et dimension
        self.view_menu.setFixedHeight(30)
        fileMenu = self.view_menu.addMenu('Fichier')
        viewMenu = self.view_menu.addMenu('Affichage')
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

        vectorAction = QAction('Afficher Vecteur vitesse des robots', self, checkable=True)
        vectorAction.triggered.connect(self.view_screen.change_vector_option)
        viewMenu.addAction(vectorAction)

        nuumbAction = QAction('Afficher Numéro des robots', self, checkable=True)
        nuumbAction.triggered.connect(self.view_screen.show_number_option)
        viewMenu.addAction(nuumbAction)

        viewMenu.addSeparator()

        fullscreenAction = QAction('Fenêtre en Plein écran', self, checkable=True)
        fullscreenAction.triggered.connect(self.toggle_fullscreen)
        fullscreenAction.setShortcut(Qt.Key_F2)
        viewMenu.addAction(fullscreenAction)

        # => Menu Outil
        StrategyControllerAction = QAction('Contrôleur de Stratégie', self,  checkable=True)
        StrategyControllerAction.triggered.connect(self.view_controller.show_hide)
        toolMenu.addAction(StrategyControllerAction)

        loggerAction = QAction('Afficher le Logger', self,  checkable=True)
        loggerAction.triggered.connect(self.view_logger.show_hide)
        toolMenu.addAction(loggerAction)

    def init_signals(self):
        signal(SIGINT, self.signal_handle)
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    def update_logging(self):
        self.view_logger.refresh()

    def save_logging(self, path):
        self.model_datain.save_logging(path)

    def aboutMsgBox(self):
        QMessageBox.about(self, 'À Propos', 'ROBOCUP ULAVAL © 2016\n\ncontact@robocupulaval.com')

    def closeEvent(self, event):
        self.close()

    def signal_handle(self, *args):
        """ Responsable du traitement des signaux """
        self.close()

    def resize_window(self):
        # self.setFixedSize(self.minimumSizeHint())
        pass
    
    def add_draw_on_screen(self, draw):
        """ Ajout un dessin sur la fenêtre du terrain """
        # TODO - Trouver un moyen de formater les coordonnées / taille pour la vue autrement
        try:
            qt_draw = self.draw_handler.get_qt_draw_object(draw)
            if qt_draw is not None:
                self.view_screen.load_draw(qt_draw)
        except:
            pass

    def set_ball_pos_on_screen(self, x, y):
        """ Modifie la position de la balle sur le terrain """
        self.view_screen.set_ball_pos(x, y)

    def set_robot_pos_on_screen(self, bot_id, pst, theta):
        """ Modifie la position et l'orientation d'un robot sur le terrain """
        self.view_screen.set_bot_pos(bot_id, *pst, theta)

    def hide_mob(self, bot_id=None):
        """ Cache l'objet mobile si l'information n'est pas update """
        if self.view_screen.isVisible() and not self.view_screen.option_vanishing:
            if bot_id is None:
                self.view_screen.hide_ball()
            else:
                self.view_screen.hide_bot(bot_id)

    def update_target_on_screen(self):
        """ Interruption pour mettre à jour les données de la cible """
        try:
            self.view_screen.update_tactic_targeting()
        except:
            pass

    def add_logging_message(self, name, message, level=2):
        self.model_datain.add_logging(name, message, level=level)

    def get_drawing_object(self, index):
        return self.draw_handler.get_specific_draw_object(index)

    def toggle_fullscreen(self):
        if not self.windowState() == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowActive)
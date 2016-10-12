# Under MIT License, see LICENSE.txt
import sys
from PyQt5.QtGui import QMainWindow
from PyQt5.QtGui import QApplication
from PyQt5.QtGui import QMenuBar
from PyQt5.QtGui import QAction
from PyQt5.QtGui import QMessageBox

__author__ = 'RoboCupULaval'


class MainWindow(QMainWindow):
    # TODO : Finir l'intégration des éléments de le fenêtre principale
    def __init__(self):
        QMainWindow.__init__(self)
        self.menubar = QMenuBar(self)
        self.init_menubar()

    def init_menubar(self):
        # Titre des menus et dimension
        fileMenu = self.menubar.addMenu('Fichier')
        viewMenu = self.menubar.addMenu('Vue')
        toolMenu = self.menubar.addMenu('Outil')
        helpMenu = self.menubar.addMenu('Aide')

        # Action et entête des sous-menus
        # => Menu Aide
        helpAction = QAction('À propos', self)
        #helpAction.triggered.connect(self.aboutMsgBox)
        helpMenu.addAction(helpAction)

        # => Menu Fichier
        exitAction = QAction('Quitter', self)
        #exitAction.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitAction)

        # => Menu Vue
        vanishAction = QAction('Afficher Vanishing', self, checkable=True)
        #vanishAction.triggered.connect(self.view_screen.change_vanish_option)
        viewMenu.addAction(vanishAction)

        nuumbAction = QAction('Afficher Numéro des robots', self, checkable=True)
        #nuumbAction.triggered.connect(self.view_screen.show_number_option)
        viewMenu.addAction(nuumbAction)

        # => Menu Outil
        StrategyControllerAction = QAction('Contrôleur de Stratégie', self, checkable=True)
        #StrategyControllerAction.triggered.connect(self.view_controller.show_hide)
        toolMenu.addAction(StrategyControllerAction)

        loggerAction = QAction('Afficher le Logger', self, checkable=True)
        #loggerAction.triggered.connect(self.view_logger.show_hide)
        toolMenu.addAction(loggerAction)

        # Création du menu bar
        self.setMenuBar(self.menubar)
# Under MIT License, see LICENSE.txt

from signal import signal, SIGINT
from time import sleep

import PyQt5
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QWidget, QMenuBar, QHBoxLayout, QVBoxLayout, \
                            QAction, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot

from Communication.GrSimReplacementSender import GrSimReplacementSender
from Model.FrameModel import FrameModel
from Model.DataInModel import DataInModel
from Model.DataOutModel import DataOutModel
from Model.RecorderModel import RecorderModel

from View.FieldView import FieldView
from View.FilterCtrlView import FilterCtrlView
from View.StrategyCtrView import StrategyCtrView
from View.LoggerView import LoggerView
from View.MainWindow import MainWindow
from View.ParamView import ParamView
from View.MediaControllerView import MediaControllerView
from View.StatusBarView import StatusBarView
from View.GameStateView import GameStateView

from Communication.UDPServer import UDPServer
from Communication.vision import Vision
from Communication.UDPConfig import UDPConfig

from Controller.DrawingObject import Color

from .DrawingObjectFactory import DrawingObjectFactory
from .QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class MainController(QWidget):
    # TODO: Dissocier Controller de la fenêtre principale
    def __init__(self, team_color, vision_port, referee_port, ui_cmd_sender_port, ui_cmd_receiver_port):
        super().__init__()

        self.team_color = team_color
        #port = QtCore.QMetaType.type('QVector<int>')
        self.receiving_port = vision_port
        # Création des Contrôleurs
        self.draw_handler = DrawingObjectFactory(self)

        # Communication
        # self.network_data_in = UDPServer(self)
        self.network_data_in = UDPServer(name='UDPServer', debug=False, rcv_port=ui_cmd_sender_port, snd_port=ui_cmd_receiver_port)
        self.network_vision = Vision(port=self.receiving_port)
        self.ai_server_is_serial = False
        self.udp_config = UDPConfig(port=self.receiving_port)
        self.grsim_sender = GrSimReplacementSender()


        # Création des Modèles
        self.model_frame = FrameModel(self)
        self.model_datain = DataInModel(self)
        self.model_dataout = DataOutModel(self)
        self.model_recorder = RecorderModel()

        # Création des Vues
        self.main_window = MainWindow()
        self.view_menu = QMenuBar(self)
        self.view_logger = LoggerView(self)
        self.view_field_screen = FieldView(self)
        self.view_filter = FilterCtrlView(self)
        self.view_param = ParamView(self)
        self.view_controller = StrategyCtrView(self)
        self.view_media = MediaControllerView(self)
        self.view_status = StatusBarView(self)
        self.view_robot_state = GameStateView(self)

        # Initialisation des UI
        self.init_main_window()
        self.init_menubar()
        self.init_signals()

        # Positions enregistrées des robots
        self.teams_formation = []

    def init_main_window(self):
        # Initialisation de la fenêtre
        self.setWindowTitle('RoboCup ULaval | GUI Debug | Team ' + self.team_color)
        self.setWindowIcon(QIcon('Img/favicon.jpg'))
        self.resize(975, 550)

        # Initialisation des Layouts
        # => Field | Filter | StratController (Horizontal)
        sub_layout = QSplitter(self)

        sub_layout.setContentsMargins(0, 0, 0, 0)
        sub_layout.addWidget(self.view_robot_state)

        # Ajout des boutons pour sauvegarder et restaurer la position des robots
        field_widget = QWidget()
        field_layout = QVBoxLayout()

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(field_widget)

        self.btn_save_teams_formation = QPushButton("Save teams formation")
        self.btn_save_teams_formation.clicked.connect(self.save_teams_formation)
        self.btn_restore_teams_formation = QPushButton("Restore teams formation")
        self.btn_restore_teams_formation.clicked.connect(self.restore_teams_formation)
        buttons_layout.addWidget(self.btn_save_teams_formation)
        buttons_layout.addWidget(self.btn_restore_teams_formation)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_widget.setLayout(buttons_layout)

        field_layout.addWidget(self.view_field_screen)
        field_layout.addWidget(buttons_widget)
        field_widget.setLayout(field_layout)

        sub_layout.addWidget(field_widget)
        sub_layout.addWidget(self.view_filter)
        sub_layout.addWidget(self.view_controller)
        QSplitter.setSizes(sub_layout, [200, 500, 100, 100])

        # => Menu | SubLayout | Media | Logger | Status (Vertical)
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.view_menu)
        top_layout.addWidget(sub_layout)
        top_layout.addWidget(self.view_media)
        top_layout.addWidget(self.view_logger)
        top_layout.addWidget(self.view_status)
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(top_layout)

        # Initialisation des modèles aux vues
        self.view_logger.set_model(self.model_datain)
        self.model_datain.setup_udp_server(self.network_data_in)
        self.model_dataout.setup_udp_server(self.network_data_in)
        self.model_frame.set_vision(self.network_vision)
        self.model_frame.start()
        self.model_frame.set_recorder(self.model_recorder)
        self.model_datain.set_recorder(self.model_recorder)


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

        paramAction = QAction('Paramètres', self)
        paramAction.triggered.connect(self.view_param.show)
        fileMenu.addAction(paramAction)

        fileMenu.addSeparator()

        exitAction = QAction('Quitter', self)
        exitAction.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitAction)

        # => Menu Vue
        fieldMenu = viewMenu.addMenu('Terrain')

        toggleFrameRate = QAction("Afficher la fréquence", self, checkable=True)
        toggleFrameRate.triggered.connect(self.view_field_screen.toggle_frame_rate)
        fieldMenu.addAction(toggleFrameRate)

        fieldMenu.addSeparator()

        flipXAction = QAction("Changer l'axe des X", self, checkable=True)
        flipXAction.triggered.connect(self.flip_screen_x_axe)
        fieldMenu.addAction(flipXAction)

        flipYAction = QAction("Changer l'axe des Y", self, checkable=True)
        flipYAction.triggered.connect(self.flip_screen_y_axe)
        fieldMenu.addAction(flipYAction)

        viewMenu.addSeparator()

        camMenu = viewMenu.addMenu('Camera')

        resetCamAction = QAction("Réinitialiser la caméra", self)
        resetCamAction.triggered.connect(self.view_field_screen.reset_camera)
        camMenu.addAction(resetCamAction)

        lockCamAction = QAction("Bloquer la caméra", self)
        lockCamAction.triggered.connect(self.view_field_screen.toggle_lock_camera)
        camMenu.addAction(lockCamAction)

        viewMenu.addSeparator()

        botMenu = viewMenu.addMenu('Robot')

        vanishAction = QAction('Afficher Vanishing', self, checkable=True)
        vanishAction.triggered.connect(self.view_field_screen.toggle_vanish_option)
        vanishAction.trigger()
        botMenu.addAction(vanishAction)

        vectorAction = QAction('Afficher Vecteur vitesse des robots', self, checkable=True)
        vectorAction.triggered.connect(self.view_field_screen.toggle_vector_option)
        botMenu.addAction(vectorAction)

        nuumbAction = QAction('Afficher Numéro des robots', self, checkable=True)
        nuumbAction.triggered.connect(self.view_field_screen.show_number_option)
        nuumbAction.trigger()
        botMenu.addAction(nuumbAction)

        viewMenu.addSeparator()

        fullscreenAction = QAction('Fenêtre en Plein écran', self, checkable=True)
        fullscreenAction.triggered.connect(self.toggle_full_screen)
        fullscreenAction.setShortcut(Qt.Key_F2)
        viewMenu.addAction(fullscreenAction)

        # => Menu Outil
        filterAction = QAction('Filtre pour dessins', self, checkable=True)
        filterAction.triggered.connect(self.view_filter.show_hide)
        toolMenu.addAction(filterAction)

        StrategyControllerAction = QAction('Contrôleur de Stratégie', self,  checkable=True)
        StrategyControllerAction.triggered.connect(self.view_controller.toggle_show_hide)
        StrategyControllerAction.trigger()
        toolMenu.addAction(StrategyControllerAction)

        toolMenu.addSeparator()

        mediaAction = QAction('Contrôleur Média', self, checkable=True)
        mediaAction.triggered.connect(self.view_media.toggle_visibility)
        toolMenu.addAction(mediaAction)

        robStateAction = QAction('État des robots', self, checkable=True)
        robStateAction.triggered.connect(self.view_robot_state.show_hide)
        robStateAction.trigger()
        toolMenu.addAction(robStateAction)

        loggerAction = QAction('Loggeur', self,  checkable=True)
        loggerAction.triggered.connect(self.view_logger.show_hide)
        toolMenu.addAction(loggerAction)

    def init_signals(self):
        signal(SIGINT, self.signal_handle)

    def update_logging(self):
        self.view_logger.refresh()

    def save_logging(self, path, texte):
        self.model_datain.write_logging_file(path, texte)

    def aboutMsgBox(self):
        QMessageBox.about(self, 'À Propos', 'ROBOCUP ULAVAL © 2016\n\ncontact@robocupulaval.com')

    @pyqtSlot(name='on_triggered')
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
        try:
            qt_draw = self.draw_handler.get_qt_draw_object(draw)
            if qt_draw is not None:
                self.view_field_screen.load_draw(qt_draw)
        except:
            pass

    def set_ball_pos_on_screen(self, x, y):
        """ Modifie la position de la balle sur le terrain """
        self.view_field_screen.set_ball_pos(x, y)

    def set_robot_pos_on_screen(self, bot_id, team_color, pst, theta):
        """ Modifie la position et l'orientation d'un robot sur le terrain """
        self.view_field_screen.set_bot_pos(bot_id, team_color, pst[0], pst[1], theta)

    def set_field_size(self, frame_geometry_field):
        """ Modifie la dimension du terrain provenant des frames de vision"""
        QtToolBox.field_ctrl.set_field_size(frame_geometry_field)

    def hide_ball(self):
        if self.view_field_screen.isVisible() and self.view_field_screen.option_vanishing:
            self.view_field_screen.hide_ball()

    def hide_mob(self, bot_id=None, team_color=None):
        """ Cache l'objet mobile si l'information n'est pas update """
        if self.view_field_screen.isVisible() and self.view_field_screen.option_vanishing:
            self.view_field_screen.hide_bot(bot_id, team_color)

    def update_target_on_screen(self):
        """ Interruption pour mettre à jour les données de la cible """
        try:
            self.view_field_screen.auto_toggle_visible_target()
        except:
            pass

    def add_logging_message(self, name, message, level=2):
        """ Ajoute un message de logging typé """
        self.model_datain.add_logging(name, message, level=level)

    def get_drawing_object(self, index):
        """ Récupère un dessin spécifique """
        return self.draw_handler.get_specific_draw_object(index)

    def toggle_full_screen(self):
        """ Déclenche le plein écran """
        if not self.windowState() == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowActive)

    def flip_screen_x_axe(self):
        """ Bascule l'axe des X de l'écran """
        QtToolBox.field_ctrl.flip_x_axe()

    def flip_screen_y_axe(self):
        """ Bascule l'axe des Y de l'écran """
        QtToolBox.field_ctrl.flip_y_axe()

    def get_list_of_filters(self):
        """ Récupère la liste des filtres d'affichage """
        name_filter = list(self.view_field_screen.draw_filterable.keys())
        name_filter += list(self.view_field_screen.multiple_points_map.keys())
        name_filter = set(name_filter)
        name_filter.add('None')
        return name_filter

    def set_list_of_filters(self, list_filter):
        """ Assigne une liste de filtres d'affichage """
        self.view_field_screen.list_filter = list_filter

    def deselect_all_robots(self):
        """ Désélectionne tous les robots sur le terrain """
        self.view_field_screen.deselect_all_robots()

    def select_robot(self, bot_id, team_color):
        """ Sélectionne le robot spécifié par l'index sur le terrain """
        self.view_field_screen.select_robot(bot_id, team_color)

    def get_tactic_controller_is_visible(self):
        """ Requête pour savoir le l'onglet de la page tactique est visible """
        return self.view_controller.page_tactic.isVisible()

    def force_tactic_controller_select_robot(self, bot_id, team_color):
        """ Force le sélection du robot indiqué par l'index dans la combobox du contrôleur tactique """
        self.view_controller.selectRobot.setCurrentIndex(bot_id)

    def get_cursor_position_from_screen(self):
        """ Récupère la position du curseur depuis le terrain """
        x, y = self.view_field_screen.get_cursor_position()
        coord_x, coord_y = QtToolBox.field_ctrl.convert_screen_to_real_pst(x, y)
        return int(coord_x), int(coord_y)

    def toggle_recorder(self, p_bool):
        """ Active/Désactive le Recorder """
        if p_bool:
            self.model_frame.enable_recorder()
            self.model_datain.enable_recorder()
        else:
            self.model_frame.disable_recorder()
            self.model_datain.disable_recorder()

    def get_fps(self):
        """ Récupère la fréquence de rafraîchissement de l'écran """
        return self.view_field_screen.get_fps()

    def get_is_serial(self):
        """ Récupère si le serveur de strategyIA est en mode serial (True) ou udp (False)"""
        return self.ai_server_is_serial

    def set_is_serial(self, is_serial):
        """ Détermine si le serveur de strategyIA est en mode serial (True) ou udp (False)"""
        self.ai_server_is_serial = is_serial

    def send_handshake(self):
        """ Envoie un HandShake au client """
        self.model_dataout.send_handshake()

    def send_ports_rs(self):
        ports_info = dict(zip(['recv_port',
                               'send_port'],
                              [self.network_data_in.get_rcv_port(),
                               self.network_data_in.get_snd_port()]))
        self.model_dataout.send_ports_rs(ports_info)

    def send_server(self):
        """ Envoie si le serveur utilisé par strategyIA est en serial (True) ou en udp (False)"""
        server_info = dict(zip(['is_serial', 'ip', 'port'],
                               [self.ai_server_is_serial,
                                self.network_vision.get_ip(),
                                self.network_vision.get_port()]))
        self.model_dataout.send_server(server_info)

    def send_udp_config(self):
        udp_config_info = dict(zip(['ip', 'port'],
                                   [self.udp_config.ip,
                                    self.udp_config.port]))
        self.model_dataout.send_udp_config(udp_config_info)

    def send_geometry(self):
        """ Envoie la géométrie du terrain """
        self.model_dataout.send_geometry(QtToolBox.field_ctrl)

    def waiting_for_robot_strategic_state(self):
        return self.model_datain.waiting_for_robot_strategic_state_event()

    def waiting_for_robot_state(self):
        return self.model_datain.waiting_for_robot_state_event()

    def waiting_for_play_info(self):
        return self.model_datain.waiting_for_play_info_event()

    def waiting_for_game_state(self):
        return self.model_datain.waiting_for_game_state_event()

    def get_team_color(self):
        return self.model_datain.get_team_color()

    # === RECORDER METHODS ===
    def recorder_is_playing(self):
        return self.model_recorder.is_playing()

    def recorder_get_cursor_percentage(self):
        return self.model_recorder.get_cursor_percentage()

    def recorder_trigger_pause(self):
        self.model_recorder.pause()

    def recorder_trigger_play(self):
        self.model_recorder.play()

    def recorder_trigger_back(self):
        self.model_recorder.back()

    def recorder_trigger_rewind(self):
        self.model_recorder.rewind()

    def recorder_trigger_forward(self):
        self.model_recorder.forward()

    def recorder_skip_to(self, value):
        self.model_recorder.skip_to(value)

    def save_teams_formation(self):
        self.teams_formation = self.view_field_screen.get_teams_formation()

    def restore_teams_formation(self):
        self.grsim_sender.set_robot_positions(self.teams_formation)

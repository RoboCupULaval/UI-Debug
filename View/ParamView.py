# Under MIT License, see LICENSE.txt

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, \
                            QGroupBox, QFormLayout, QLineEdit, QLabel, \
                            QPushButton, QHBoxLayout, QRadioButton
from PyQt5 import QtCore
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class ParamView(QDialog):
    def __init__(self, controller):
        self._ctrl = controller
        super().__init__(controller)
        self._layout = QVBoxLayout()
        self._pages = QTabWidget(self)
        self._page_dimension = QWidget(self)
        self._page_network = QWidget(self)
        self.init_ui()
        self.init_page_network()
        self.init_page_dimension()
        self.init_bottom_page()

    def init_ui(self):
        self._layout.addWidget(self._pages)
        self._pages.addTab(self._page_dimension, 'Dimensions')
        self._pages.addTab(self._page_network, 'Réseau')

        self.setWindowTitle('Paramètres')
        self.move(150, 150)
        self.setLayout(self._layout)

    def init_page_network(self):
        layout_main = QVBoxLayout(self._page_network)
        layout_main.setAlignment(QtCore.Qt.AlignTop)
        self._page_network.setLayout(layout_main)

        # PARAM UI Server
        group_server = QGroupBox('UI Server')
        layout_main.addWidget(group_server)
        layout_form = QFormLayout()
        group_server.setLayout(layout_form)

        # => Port rcv
        self.form_network_recv_port = QLineEdit()
        layout_form.addRow(QLabel("Port de réception :"), self.form_network_recv_port)
        # => Port snd
        self.form_network_send_port = QLineEdit()
        layout_form.addRow(QLabel("Port d'envoi :"), self.form_network_send_port)
        # => Bouton envoie des ports recv et send
        but_send_ports_rs = QPushButton('Envoyer les paramètres')
        but_send_ports_rs.clicked.connect(self._ctrl.send_ports_rs)
        layout_form.addRow(but_send_ports_rs)

        # PARAM VISION
        group_vision = QGroupBox('Vision')
        layout_main.addWidget(group_vision)
        layout_form = QFormLayout()
        group_vision.setLayout(layout_form)

        # => IP
        self.form_network_vision_ip = QLineEdit()
        layout_form.addRow(QLabel("IP :"), self.form_network_vision_ip)

        # => Port
        self.form_network_vision_port = QLineEdit()
        layout_form.addRow(QLabel("Port :"), self.form_network_vision_port)

        # => UDP/Serial
        self.form_network_vision_udp = QRadioButton()
        self.form_network_vision_udp.setChecked(True)
        self.form_network_vision_udp_label = QLabel("UDP :")
        layout_form.addRow(self.form_network_vision_udp_label, self.form_network_vision_udp)

        self.form_network_vision_serial = QRadioButton()
        self.form_network_vision_serial.toggled.connect(self.toggle_udp_config)
        layout_form.addRow(QLabel("Serial :"), self.form_network_vision_serial)

        but_send_server = QPushButton('Envoyer les paramètres du réseau')
        but_send_server.clicked.connect(self._ctrl.send_server)
        layout_form.addRow(but_send_server)

        # PARAM UI Server
        group_udp_serial = QGroupBox('Configuration UDP/Serial')
        layout_main.addWidget(group_udp_serial)
        layout_form = QFormLayout()
        group_udp_serial.setLayout(layout_form)

        # => IP Multicast UDP
        self.form_udp_multicast_ip = QLineEdit()
        layout_form.addRow(QLabel("IP Multicast:"), self.form_udp_multicast_ip)
        # => Port Multicast UDP
        self.form_udp_multicast_port = QLineEdit()
        layout_form.addRow(QLabel("Port Multicast:"), self.form_udp_multicast_port)
        # => Bouton envoie configuration UDP
        but_send_udp_multicast = QPushButton('Envoyer les paramètres de l\'UDP')
        but_send_udp_multicast.clicked.connect(self._ctrl.send_udp_config)
        layout_form.addRow(but_send_udp_multicast)


    def init_page_dimension(self):
        layout_main = QVBoxLayout(self._page_dimension)
        self._page_dimension.setLayout(layout_main)

        # Changement des dimensions du terrain
        group_field = QGroupBox('Dimensions')
        layout_main.addWidget(group_field)
        layout_field = QFormLayout()
        group_field.setLayout(layout_field)

        # => Taille du terrain (Longueur / Hauteur)
        layout_field.addRow(QLabel('\nDimension du Terrain'))
        self.form_field_length = QLineEdit()
        layout_field.addRow(QLabel('largeur :'), self.form_field_length)
        self.form_field_width = QLineEdit()
        layout_field.addRow(QLabel('hauteur :'), self.form_field_width)

        # => Taille du but (Longueur / Hauteur)
        layout_field.addRow(QLabel('\nDimension des Buts'))
        self.form_goal_depth = QLineEdit()
        layout_field.addRow(QLabel('largeur :'), self.form_goal_depth)
        self.form_goal_width = QLineEdit()
        layout_field.addRow(QLabel('hauteur :'), self.form_goal_width)

        # => Taille de la zone de réparation (Rayon / Ligne)
        layout_field.addRow(QLabel('\nZone des buts'))
        self.form_goal_radius = QLineEdit()
        layout_field.addRow(QLabel('rayon :'), self.form_goal_radius)
        self.form_goal_line = QLineEdit()
        layout_field.addRow(QLabel('hauteur :'), self.form_goal_line)

        # => Taille de la zone centrale (Rayon)
        layout_field.addRow(QLabel('\nRayon central'))
        self.form_center_radius = QLineEdit()
        layout_field.addRow(QLabel('rayon :'), self.form_center_radius)

        # Changement de ratio Mobs / Terrain
        layout_field.addRow(QLabel('\nRatio Terrain/Mobs'))
        self.form_ratio_mobs = QLineEdit()
        layout_field.addRow(QLabel('ratio :'), self.form_ratio_mobs)

        self.restore_values()

        but_send_geometry = QPushButton('Envoyer la Géométrie du terrain')
        but_send_geometry.clicked.connect(self._ctrl.send_geometry)
        layout_field.addRow(but_send_geometry)

    def init_bottom_page(self):
        # Bas de fenêtre
        layout_bottom = QHBoxLayout()
        self._layout.addLayout(layout_bottom)

        # => Bouton OK
        but_ok = QPushButton('Ok')
        but_ok.clicked.connect(self._apply_param_and_leave)
        layout_bottom.addWidget(but_ok)

        # => Bouton Annuler
        but_cancel = QPushButton('Annuler')
        but_cancel.clicked.connect(self.hide)
        layout_bottom.addWidget(but_cancel)

        # => Bouton Appliquer
        but_apply = QPushButton('Appliquer')
        but_apply.clicked.connect(self._apply_param)
        layout_bottom.addWidget(but_apply)

        # => Bouton Défaut
        but_default = QPushButton('Défaut')
        but_default.setStyleSheet("QPushButton {font:italic}")
        but_default.clicked.connect(self.restore_default_values)
        layout_bottom.addWidget(but_default)

    def _apply_param_and_leave(self):
        if self._apply_param():
            self.hide()

    def restore_default_values(self):
        # FIELD DIMENSION
        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs_default))

        # NETWORK
        self.form_network_recv_port.setText(str(self._ctrl.network_data_in.get_default_rcv_port()))
        self.form_network_send_port.setText(str(self._ctrl.network_data_in.get_default_snd_port()))
        self.form_network_vision_ip.setText(str(self._ctrl.network_vision.get_default_ip()))
        self.form_network_vision_port.setText(str(self._ctrl.network_vision.get_default_port()))
        self.form_network_vision_serial.setChecked(False)
        self.form_network_vision_udp.setChecked(True)
        self.form_udp_multicast_ip.setText(str(self._ctrl.udp_config.get_default_ip()))
        self.form_udp_multicast_ip.setDisabled(False)
        self.form_udp_multicast_port.setText(str(self._ctrl.udp_config.get_default_port()))
        self.form_udp_multicast_port.setDisabled(False)

        self._apply_param()

    def restore_values(self):
        self.form_field_length.setText(str(QtToolBox.field_ctrl.field_length))
        self.form_field_width.setText(str(QtToolBox.field_ctrl.field_width))

        self.form_goal_depth.setText(str(QtToolBox.field_ctrl.goal_depth))
        self.form_goal_width.setText(str(QtToolBox.field_ctrl.goal_width))

        self.form_goal_radius.setText(str(QtToolBox.field_ctrl.defense_radius))
        self.form_goal_line.setText(str(QtToolBox.field_ctrl.defense_stretch))

        self.form_center_radius.setText(str(QtToolBox.field_ctrl.center_circle_radius))

        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs))

        self.form_network_recv_port.setText(str(self._ctrl.network_data_in.get_rcv_port()))
        self.form_network_send_port.setText(str(self._ctrl.network_data_in.get_snd_port()))
        self.form_network_vision_ip.setText(str(self._ctrl.network_vision.get_ip()))
        self.form_network_vision_port.setText(str(self._ctrl.network_vision.get_port()))
        self.form_udp_multicast_ip.setText(str(self._ctrl.udp_config.ip))
        self.form_udp_multicast_port.setText(str(self._ctrl.udp_config.port))

    def toggle_udp_config(self):
        if self.form_network_vision_serial.isChecked():
            self.form_udp_multicast_ip.setDisabled(True)
            self.form_udp_multicast_port.setDisabled(True)
        else:
            self.form_udp_multicast_ip.setDisabled(False)
            self.form_udp_multicast_port.setDisabled(False)

    def hide(self):
        self.restore_values()
        self._apply_param()
        super().hide()

    def _apply_param(self):
        is_wrong = False
        style_bad = "QLineEdit {background: rgb(255, 100, 100)}"
        style_good = "QLineEdit {background: rgb(255, 255, 255)}"

        try:
            self.form_field_length.setStyleSheet(style_good)
            QtToolBox.field_ctrl.field_length = int(self.form_field_length.text())
        except Exception as e:
            self.form_field_length.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_field_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.field_width = int(self.form_field_width.text())
        except Exception as e:
            self.form_field_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_depth.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_depth = int(self.form_goal_depth.text())
        except Exception as e:
            self.form_goal_depth.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_width = int(self.form_goal_width.text())
        except Exception as e:
            self.form_goal_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_center_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.center_circle_radius = int(self.form_center_radius.text())
        except Exception as e:
            self.form_center_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.defense_radius = int(self.form_goal_radius.text())
        except Exception as e:
            self.form_goal_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_line.setStyleSheet(style_good)
            QtToolBox.field_ctrl.defense_stretch = int(self.form_goal_line.text())
        except Exception as e:
            self.form_goal_line.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_ratio_mobs.setStyleSheet(style_good)
            QtToolBox.field_ctrl.ratio_field_mobs = float(self.form_ratio_mobs.text())
        except Exception as e:
            print(e)
            self.form_ratio_mobs.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_network_recv_port.setStyleSheet(style_good)
            if not self._ctrl.network_data_in.get_rcv_port() == int(self.form_network_recv_port.text()):
                self._ctrl.network_data_in.new_rcv_connexion(int(self.form_network_recv_port.text()))
        except Exception as e:
            self.form_network_recv_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_network_send_port.setStyleSheet(style_good)
            if not self._ctrl.network_data_in.get_snd_port() == int(self.form_network_send_port.text()):
                self._ctrl.network_data_in.set_snd_port(int(self.form_network_send_port.text()))
        except Exception as e:
            self.form_network_send_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_network_vision_ip.setStyleSheet(style_good)
            self.form_network_recv_port.setStyleSheet(style_good)
            if not self._ctrl.network_vision.get_ip() == str(self.form_network_vision_ip.text()) \
                or not self._ctrl.network_vision.get_port() == int(self.form_network_vision_port.text()):
                self._ctrl.network_vision.set_new_connexion(str(self.form_network_vision_ip.text()),
                                                            int(self.form_network_vision_port.text()))
        except Exception as e:
            self.form_network_vision_ip.setStyleSheet(style_bad)
            self.form_network_vision_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_network_vision_serial.setStyleSheet(style_good)
            self.form_network_vision_udp_label.setStyleSheet(style_good)
            if self._ctrl.get_is_serial != self.form_network_vision_serial.isChecked():
                self._ctrl.set_is_serial(self.form_network_vision_serial.isChecked())
            self.toggle_udp_config()
        except Exception as e:
            self.form_network_vision_serial.setStyleSheet(style_bad)
            self.form_network_vision_udp_label.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_udp_multicast_ip.setStyleSheet(style_good)
            if self._ctrl.udp_config.ip != str(self.form_udp_multicast_ip.text()):
                self._ctrl.udp_config.ip = self.form_udp_multicast_ip.text()
            self.toggle_udp_config()
        except Exception as e:
            self.form_udp_multicast_ip.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_udp_multicast_port.setStyleSheet(style_good)
            if self._ctrl.udp_config.port != str(self.form_udp_multicast_port.text()):
                self._ctrl.udp_config.port = self.form_udp_multicast_port.text()
        except Exception as e:
            self.form_udp_multicast_port.setStyleSheet(style_bad)
            is_wrong = True

        if is_wrong:
            return False
        else:
            return True

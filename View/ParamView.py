# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui
from PyQt4 import QtCore
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class ParamView(QtGui.QDialog):
    def __init__(self, controller):
        self._ctrl = controller
        super().__init__(controller)
        self._layout = QtGui.QVBoxLayout()
        self._pages = QtGui.QTabWidget(self)
        self._page_dimension = QtGui.QWidget(self)
        self._page_network = QtGui.QWidget(self)
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
        layout_main = QtGui.QVBoxLayout(self._page_network)
        layout_main.setAlignment(QtCore.Qt.AlignTop)
        self._page_network.setLayout(layout_main)

        # PARAM UI Server
        group_server = QtGui.QGroupBox('UI Server')
        layout_main.addWidget(group_server)
        layout_form = QtGui.QFormLayout()
        group_server.setLayout(layout_form)

        # => Port rcv
        self.form_network_recv_port = QtGui.QLineEdit()
        layout_form.addRow(QtGui.QLabel("Port de réception :"), self.form_network_recv_port)
        # => Port snd
        self.form_network_send_port = QtGui.QLineEdit()
        layout_form.addRow(QtGui.QLabel("Port d'envoi :"), self.form_network_send_port)

        # PARAM VISION
        group_vision = QtGui.QGroupBox('Vision')
        layout_main.addWidget(group_vision)
        layout_form = QtGui.QFormLayout()
        group_vision.setLayout(layout_form)

        # => IP
        self.form_network_vision_ip = QtGui.QLineEdit()
        self.form_network_vision_ip.setDisabled(True)
        layout_form.addRow(QtGui.QLabel("IP :"), self.form_network_vision_ip)
        # => Port
        self.form_network_vision_port = QtGui.QLineEdit()
        layout_form.addRow(QtGui.QLabel("Port :"), self.form_network_vision_port)

    def init_page_dimension(self):
        layout_main = QtGui.QVBoxLayout(self._page_dimension)
        self._page_dimension.setLayout(layout_main)

        # Changement des dimensions du terrain
        group_field = QtGui.QGroupBox('Dimensions')
        layout_main.addWidget(group_field)
        layout_field = QtGui.QFormLayout()
        group_field.setLayout(layout_field)

        # => Taille du terrain (Longueur / Hauteur)
        layout_field.addRow(QtGui.QLabel('\nDimension du Terrain'))
        self.form_field_width = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('largeur :'), self.form_field_width)
        self.form_field_height = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('hauteur :'), self.form_field_height)

        # => Taille du but (Longueur / Hauteur)
        layout_field.addRow(QtGui.QLabel('\nDimension des Buts'))
        self.form_goal_width = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('largeur :'), self.form_goal_width)
        self.form_goal_height = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('hauteur :'), self.form_goal_height)

        # => Taille de la zone de réparation (Rayon / Ligne)
        layout_field.addRow(QtGui.QLabel('\nZone des buts'))
        self.form_goal_radius = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('rayon :'), self.form_goal_radius)
        self.form_goal_line = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('hauteur :'), self.form_goal_line)

        # => Taille de la zone centrale (Rayon)
        layout_field.addRow(QtGui.QLabel('\nRayon central'))
        self.form_center_radius = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('rayon :'), self.form_center_radius)

        # Changement de ratio Mobs / Terrain
        layout_field.addRow(QtGui.QLabel('\nRatio Terrain/Mobs'))
        self.form_ratio_mobs = QtGui.QLineEdit()
        layout_field.addRow(QtGui.QLabel('ratio :'), self.form_ratio_mobs)

        self.restore_values()

        but_send_geometry = QtGui.QPushButton('Envoyer la Géométrie du terrain')
        but_send_geometry.clicked.connect(self._ctrl.send_geometry)
        layout_field.addRow(but_send_geometry)

    def init_bottom_page(self):
        # Bas de fenêtre
        layout_bottom = QtGui.QHBoxLayout()
        self._layout.addLayout(layout_bottom)

        # => Bouton OK
        but_ok = QtGui.QPushButton('Ok')
        but_ok.clicked.connect(self._apply_param_and_leave)
        layout_bottom.addWidget(but_ok)

        # => Bouton Annuler
        but_cancel = QtGui.QPushButton('Annuler')
        but_cancel.clicked.connect(self.hide)
        layout_bottom.addWidget(but_cancel)

        # => Bouton Appliquer
        but_apply = QtGui.QPushButton('Appliquer')
        but_apply.clicked.connect(self._apply_param)
        layout_bottom.addWidget(but_apply)

        # => Bouton Défaut
        but_default = QtGui.QPushButton('Défaut')
        but_default.setStyleSheet("QPushButton {font:italic}")
        but_default.clicked.connect(self.restore_default_values)
        layout_bottom.addWidget(but_default)

    def _apply_param_and_leave(self):
        if self._apply_param():
            self.hide()

    def restore_default_values(self):
        # FIELD DIMENSION
        self.form_field_width.setText(str(QtToolBox.field_ctrl.size_default[0]))
        self.form_field_height.setText(str(QtToolBox.field_ctrl.size_default[1]))
        self.form_goal_width.setText(str(QtToolBox.field_ctrl.goal_size_default[0]))
        self.form_goal_height.setText(str(QtToolBox.field_ctrl.goal_size_default[1]))
        self.form_goal_radius.setText(str(QtToolBox.field_ctrl.goal_radius_default))
        self.form_goal_line.setText(str(QtToolBox.field_ctrl.goal_line_default))
        self.form_center_radius.setText(str(QtToolBox.field_ctrl.radius_center_default))
        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs_default))

        # NETWORK
        self.form_network_recv_port.setText(str(self._ctrl.network_data_in.get_default_rcv_port()))
        self.form_network_snd_port.setText(str(self._ctrl.network_data_in.get_default_snd_port()))
        self.form_network_vision_ip.setText(str(self._ctrl.network_vision.get_default_ip()))
        self.form_network_vision_port.setText(str(self._ctrl.network_vision.get_default_port()))

        self._apply_param()

    def restore_values(self):
        self.form_field_width.setText(str(QtToolBox.field_ctrl.size[0]))
        self.form_field_height.setText(str(QtToolBox.field_ctrl.size[1]))

        self.form_goal_width.setText(str(QtToolBox.field_ctrl.goal_size[0]))
        self.form_goal_height.setText(str(QtToolBox.field_ctrl.goal_size[1]))

        self.form_goal_radius.setText(str(QtToolBox.field_ctrl.goal_radius))
        self.form_goal_line.setText(str(QtToolBox.field_ctrl.goal_line))

        self.form_center_radius.setText(str(QtToolBox.field_ctrl.radius_center))

        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs))

        self.form_network_recv_port.setText(str(self._ctrl.network_data_in.get_rcv_port()))
        self.form_network_send_port.setText(str(self._ctrl.network_data_in.get_snd_port()))
        self.form_network_vision_ip.setText(str(self._ctrl.network_vision.get_ip()))
        self.form_network_vision_port.setText(str(self._ctrl.network_vision.get_port()))

    def hide(self):
        self.restore_values()
        self._apply_param()
        super().hide()

    def _apply_param(self):
        is_wrong = False
        style_bad = "QLineEdit {background: rgb(255, 100, 100)}"
        style_good = "QLineEdit {background: rgb(255, 255, 255)}"

        try:
            self.form_field_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.size[0] = int(self.form_field_width.text())
        except Exception as e:
            self.form_field_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_field_height.setStyleSheet(style_good)
            QtToolBox.field_ctrl.size[1] = int(self.form_field_height.text())
        except Exception as e:
            self.form_field_height.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_size[0] = int(self.form_goal_width.text())
        except Exception as e:
            self.form_goal_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_height.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_size[1] = int(self.form_goal_height.text())
        except Exception as e:
            self.form_goal_height.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_center_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.radius_center = int(self.form_center_radius.text())
        except Exception as e:
            self.form_center_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_radius = int(self.form_goal_radius.text())
        except Exception as e:
            self.form_goal_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_line.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_line = int(self.form_goal_line.text())
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
            print(type(e).__name__, e)
            self.form_network_vision_ip.setStyleSheet(style_bad)
            self.form_network_vision_port.setStyleSheet(style_bad)
            is_wrong = True

        if is_wrong:
            return False
        else:
            return True
# Under MIT License, see LICENSE.txt

import math
from time import sleep

from PyQt4 import QtGui
from PyQt4 import QtCore

from Controller.DrawQtObject.QtToolBox import QtToolBox
__author__ = 'RoboCupULaval'


class FieldView(QtGui.QWidget):
    frame_rate = 60

    def __init__(self, controller):
        QtGui.QWidget.__init__(self)
        self.init_window()
        self.controller = controller
        self.last_frame = 0
        self.timer_screen_update = QtCore.QTimer()
        self.graph_mobs = dict()
        self.graph_draw = dict()

        # Option
        self.option_vanishing = True
        self.option_show_number = False
        self.option_target_mode = False

        # Targeting
        self.last_target = None

        # Thread
        self._emit_signal = QtCore.pyqtSignal
        self._mutex = QtCore.QMutex()

        # Initialisation de l'interface
        self.init_graph_mobs()
        self.init_view_event()
        self.show()

    def init_view_event(self):
        self.timer_screen_update.timeout.connect(self.update_custom)
        self.timer_screen_update.start((1 / self.frame_rate) * 1000)

    def update_custom(self):
        self._emit_signal()
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBackground(QtToolBox.create_brush())
        # self.draw_effects(painter)
        self.draw_field(painter)
        self.draw_mobs(painter)
        painter.end()

    def draw_effects(self, painter):
        for effect in self.graph_draw['notset']:
            effect.draw(painter)

    def draw_field(self, painter):
        self.graph_draw['field'].draw(painter)

    def draw_mobs(self, painter):
        for mobs in self.graph_mobs.values():
            if isinstance(mobs, list):
                for mob in mobs:
                    mob.draw(painter)
            else:
                mobs.draw(painter)

    def mousePressEvent(self, event):
        if self.controller.view_controller.isVisible() and self.controller.view_controller.page_tactic.isVisible():
            x, y = self.controller.field_handler.convert_screen_to_real_pst(event.pos().x(), event.pos().y())
            self.controller.model_dataout.target = (x, y)
            x, y, _ = self.controller.field_handler.convert_real_to_scene_pst(x, y)
            self.graph_mobs['target'].setPos(x, y)

    def init_window(self):
        """ Initialisation de la fenêtre du widget qui affiche le terrain"""
        self.setFixedSize(950, 650)
        self.setGeometry(0, 0, 950, 650)

    def init_graph_mobs(self):
        """ Initialisation des objets graphiques """

        # Élément graphique pour les dessins
        self.graph_draw['field'] = self.controller.get_drawing_object('field')
        self.graph_draw['field'].show()
        self.graph_draw['notset'] = list()
        self.graph_draw['robots_yellow'] = [list() for _ in range(6)]
        self.graph_draw['robots_blue'] = [list() for _ in range(6)]

        # Élément mobile graphique (Robot et balle)
        self.graph_mobs['ball'] = self.controller.get_drawing_object('ball')
        self.graph_mobs['ball'].show()
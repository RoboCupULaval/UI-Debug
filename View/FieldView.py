# Under MIT License, see LICENSE.txt

from time import time

from PyQt4 import QtCore
from PyQt4 import QtGui

from Controller.QtToolBox import QtToolBox
from Controller.DrawQtObject.InfluenceMapQtObject import InfluenceMapQtObject

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
        self.graph_map = None

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
        self.timeout_manager()
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBackground(QtToolBox.create_brush())
        self.draw_field_ground(painter)
        self.draw_map(painter)
        self.draw_effects(painter)
        self.draw_field_lines(painter)
        self.draw_mobs(painter)
        painter.end()

    def timeout_manager(self):
        ref_time = time()
        if self.graph_map is not None and self.graph_map.time_is_up(ref_time):
            self.graph_map = None

        temp_list_draw = []
        for elem in self.graph_draw['notset']:
            if not elem.time_is_up(ref_time):
                temp_list_draw.append(elem)
        self.graph_draw['notset'] = temp_list_draw


    def draw_map(self, painter):
        if self.graph_map is not None:
            self.graph_map.draw(painter)

    def draw_field_lines(self, painter):
        self.graph_draw['field-lines'].draw(painter)

    def draw_effects(self, painter):
        for effect in self.graph_draw['notset']:
            effect.draw(painter)

    def draw_field_ground(self, painter):
        self.graph_draw['field-ground'].draw(painter)

    def draw_mobs(self, painter):
        self.graph_mobs['ball'].draw(painter)
        self.graph_mobs['target'].draw(painter)
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            mob.draw(painter)

    def mousePressEvent(self, event):
        if self.controller.view_controller.isVisible() and self.controller.view_controller.page_tactic.isVisible():
            x, y = self.controller.field_handler.convert_screen_to_real_pst(event.pos().x(), event.pos().y())
            self.controller.model_dataout.target = (x, y)
            self.graph_mobs['target'].setPos(x, y)

    def init_window(self):
        """ Initialisation de la fenêtre du widget qui affiche le terrain"""
        self.setFixedSize(950, 650)
        self.setGeometry(0, 0, 950, 650)

    def init_graph_mobs(self):
        """ Initialisation des objets graphiques """

        # Élément graphique pour les dessins
        self.graph_draw['field-ground'] = self.controller.get_drawing_object('field-ground')()
        self.graph_draw['field-ground'].show()
        self.graph_draw['field-lines'] = self.controller.get_drawing_object('field-lines')()
        self.graph_draw['field-lines'].show()
        self.graph_draw['notset'] = list()
        self.graph_draw['robots_yellow'] = [list() for _ in range(6)]
        self.graph_draw['robots_blue'] = [list() for _ in range(6)]

        # Élément mobile graphique (Robots, balle et cible)
        self.graph_mobs['ball'] = self.controller.get_drawing_object('ball')()
        self.graph_mobs['robots_yellow'] = [self.controller.get_drawing_object('robot')(x, is_yellow=True) for x in range(6)]
        self.graph_mobs['robots_blue'] = [self.controller.get_drawing_object('robot')(x, is_yellow=False) for x in range(6, 12)]
        self.graph_mobs['target'] = self.controller.get_drawing_object('target')()
        # TODO : show // init setters

    def set_ball_pos(self, x, y):
        """ Modifie la position de la balle sur la fenêtre du terrain """
        if not self.graph_mobs['ball'].getX() == x and not self.graph_mobs['ball'].getY() == y:
            self.graph_mobs['ball'].setPos(x, y)
        self.graph_mobs['ball'].show()

    def set_bot_pos(self, bot_id, x, y, theta):
        """ Modifie la position et l'orientation d'un robot sur la fenêtre du terrain """
        if 0 <= bot_id < 6:
            if not self.graph_mobs['robots_yellow'][bot_id].getX() == x and \
                    not self.graph_mobs['robots_yellow'][bot_id].getY() == y:
                self.graph_mobs['robots_yellow'][bot_id].setPos(x, y)
                self.graph_mobs['robots_yellow'][bot_id].setRotation(theta)
        elif 6 <= bot_id < 12:
            if not self.graph_mobs['robots_blue'][bot_id - 6].getX() == x and \
                    not self.graph_mobs['robots_blue'][bot_id - 6].getY() == y:
                self.graph_mobs['robots_blue'][bot_id - 6].setPos(x, y)
                self.graph_mobs['robots_blue'][bot_id - 6].setRotation(theta)
        self.show_bot(bot_id)

    def hide_ball(self):
        """ Cache la balle dans la fenêtre de terrain """
        self.graph_mobs['ball'].hide()

    def hide_bot(self, bot_id):
        """ Cache un robot dans la fenêtre de terrain """
        if 0 <= bot_id < 6:
            self.graph_mobs['robots_yellow'][bot_id].hide()
            self.graph_mobs['robots_numbers'][bot_id].hide()
        elif 6 <= bot_id < 12:
            self.graph_mobs['robots_blue'][bot_id - 6].hide()
            self.graph_mobs['robots_numbers'][bot_id].hide()

    def show_ball(self):
        """ Affiche la balle dans la fenêtre de terrain """
        self.graph_mobs['ball'].show()

    def show_bot(self, bot_id):
        """ Affiche un robot dans la fenêtre du terrain """
        if 0 <= bot_id < 6:
            self.graph_mobs['robots_yellow'][bot_id].show()
        elif 6 <= bot_id < 12:
            self.graph_mobs['robots_blue'][bot_id - 6].show()

    def show_number_option(self):
        ''' Affiche les numéros des robots '''
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            if mob.number_isVisible():
                mob.hide_number()
            else:
                mob.show_number()

    def change_vanish_option(self):
        self.option_vanishing = not self.option_vanishing

    def update_tactic_targeting(self):
        # TODO refaire en passant par une méthode du MainController
        if self.controller.view_controller.isVisible() and self.controller.view_controller.page_tactic.isVisible():
            self.graph_mobs['target'].show()
        else:
            self.graph_mobs['target'].hide()

    def load_draw(self, draw):
        draw.show()
        if isinstance(draw, InfluenceMapQtObject):
            self.graph_map = draw
        else:
            self.graph_draw['notset'].append(draw)

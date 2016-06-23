# Under MIT License, see LICENSE.txt

import math

from PyQt4.QtGui import *
from PyQt4.QtCore import *

__author__ = 'RoboCupULaval'


class FieldView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.parent = parent
        self.scene = QGraphicsScene(self)
        self.model = None
        self.last_frame = 0
        self.graph_mobs = dict()
        self.graph_draw = dict()

        # Initialisation de l'interface
        self.init_draw_tools()
        self.init_graph_mobs()

        self.init_window()
        self.draw_field()

        # Option
        self.option_vanishing = True
        self.option_show_number = False
        self.option_target_mode = False

        # Targeting
        self.last_target = None

    def set_model(self, model):
        """ Ajoute le modèle de la vue """
        self.model = model
        self.scene.addItem(self.graph_mobs['ball'])
        self.scene.addItem(self.graph_mobs['target'])
        for graphic_bot in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            self.scene.addItem(graphic_bot)
        for number in self.graph_mobs['robots_numbers']:
            self.scene.addItem(number)

    def mousePressEvent(self, event):
        if self.parent.view_controller.isVisible() and self.parent.view_controller.page_tactic.isVisible():
            x, y = self.model.field_info.convert_screen_to_real_pst(event.pos().x(), event.pos().y())
            self.parent.model_dataout.target = (x, y)
            x, y, _ = self.model.field_info.convert_real_to_scene_pst(x, y)
            self.graph_mobs['target'].setPos(x, y)

    def draw_field(self):
        """ Dessine le terrain et ses contours """
        self.scene.setSceneRect(-475, -325, 950, 650)

        # Dessin des lignes de délimitations du terrain
        self.scene.addRect(-450, -300, 900, 600, self.white_pen)
        self.scene.addLine(0, 300, 0, -300, self.white_pen)
        self.scene.addEllipse(-50, -50, 100, 100, self.white_pen)

    def init_draw_tools(self):
        """ Initialisation des outils de dessin """
        self.white_pen = QPen(Qt.white)
        self.red_pen = QPen(Qt.red)
        self.btn_clear = QPushButton()
        self.btn_clear.setIcon(QIcon('Img/map_delete.png'))
        self.btn_clear.pressed.connect(self.clear_drawing)
        self.btn_clear.setGeometry(-450, 310, 30, 30)
        self.scene.addWidget(self.btn_clear)

    def init_window(self):
        """ Initialisation de la fenêtre du widget qui affiche le terrain"""
        self.setFixedSize(1000, 700)
        self.scene.setSceneRect(-475, -325, 950, 650)
        self.scene.setBackgroundBrush(Qt.darkGreen)
        self.setScene(self.scene)

    def init_graph_mobs(self):
        """ Initialisation des objets graphiques """
        # Élément graphique pour les dessins
        self.graph_draw['notset'] = list()
        self.graph_draw['robots_yellow'] = [list() for _ in range(6)]
        self.graph_draw['robots_blue'] = [list() for _ in range(6)]

        # Élément graphique de la balle
        self.graph_mobs['ball'] = QGraphicsEllipseItem(-2.15, -2.15, 4.3, 4.3)
        self.graph_mobs['ball'].setBrush(QBrush(QColor(255, 92, 0)))
        self.graph_mobs['ball'].setPen(QPen(QColor(255, 92, 0)))
        self.graph_mobs['ball'].setZValue(10)
        self.graph_mobs['ball'].hide()

        # Élément graphique de la cible
        self.graph_mobs['target'] = QGraphicsPixmapItem(QPixmap('Img/ico-target.png'))
        self.graph_mobs['target'].setOffset(-55, -55)
        self.graph_mobs['target'].scale(0.21, 0.21)
        self.graph_mobs['target'].hide()
        self.graph_mobs['target'].setZValue(10)

        # Élément graphique des robots jaunes
        self.graph_mobs['robots_yellow'] = [QGraphicsEllipseItem(-11.25, -11.25, 22.5, 22.5) for _ in range(6)]
        for robot_yellow in self.graph_mobs['robots_yellow']:
            robot_yellow.hide()
            robot_yellow.setZValue(10)
            robot_yellow.setSpanAngle(50000)
            robot_yellow.setBrush(QBrush(QColor(255, 255, 105)))
            robot_yellow.setPen(QPen(QColor(0, 0, 0)))

        # Élément graphique des robots bleus
        self.graph_mobs['robots_blue'] = [QGraphicsEllipseItem(-11.25, -11.5, 22.5, 22.5) for _ in range(6)]
        for robots_blue in self.graph_mobs['robots_blue']:
            robots_blue.hide()
            robots_blue.setZValue(10)
            robots_blue.setSpanAngle(50000)
            robots_blue.setBrush(QBrush(QColor(105, 255, 255)))
            robots_blue.setPen(QPen(QColor(0, 0, 0)))

        # Élément graphique des nombres au dessus des robots
        self.graph_mobs['robots_numbers'] = [QGraphicsTextItem(str(x)) for x in range(12)]
        for number in self.graph_mobs['robots_numbers']:
            font = QFont()
            font.setBold(True)
            number.setZValue(10)
            number.setFont(font)
            number.setPos(-6666, -6666)
            number.hide()

    def change_vanish_option(self):
        """ Option qui rend apparent la disparition des robots """
        self.option_vanishing = not self.option_vanishing

    def show_number_option(self):
        """ Option qui affiche ou cache les numéros des robots """
        self.option_show_number = not self.option_show_number

    def clear_drawing(self):
        """ Efface les dessins sur le terrain """
        reply = QMessageBox.warning(self.parent, 'Suppression des dessins', 'Êtes-vous sûr de vouloir effacer tous les '
                                     'dessins sur le terrain ?', QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            for qt_item in self.graph_draw['notset']:
                self.scene.removeItem(qt_item)
            self.graph_draw['notset'].clear()

            for list_item in self.graph_draw['robots_blue'] + self.graph_draw['robots_yellow']:
                for qt_item in list_item:
                    self.scene.removeItem(qt_item)

            self.graph_draw['robots_yellow'].clear()
            self.graph_draw['robots_blue'].clear()

    def load_draw(self, qt_obj, type=None):
        """ Charge un dessin sur le terrain """
        if type is None:
            self.graph_draw['notset'].append(qt_obj)
        elif 0 <= type < 6:
            self.graph_draw['robots_yellow'].append(qt_obj)
        elif 6 <= type < 12:
            self.graph_draw['robots_blue'].append(qt_obj)

        self.scene.addItem(qt_obj)

    def set_ball_pos(self, x, y):
        """ Modifie la position de la balle sur la fenêtre du terrain """
        if not self.graph_mobs['ball'].isVisible():
            self.show_ball()
        if not self.graph_mobs['ball'].pos().x() == x and not self.graph_mobs['ball'].pos().y() == y:
            self.graph_mobs['ball'].setPos(x, y)

    def set_bot_pos(self, bot_id, x, y, theta):
        """ Modifie la position et l'orientation d'un robot sur la fenêtre du terrain """
        if 0 <= bot_id < 6:
            if not self.graph_mobs['robots_yellow'][bot_id].pos().x() == x and \
                    not self.graph_mobs['robots_yellow'][bot_id].pos().y() == y:
                self.graph_mobs['robots_yellow'][bot_id].setPos(x, y)
                self.graph_mobs['robots_yellow'][bot_id].setRotation(math.radians(theta))
                self.graph_mobs['robots_numbers'][bot_id].setPos(x, y)
        elif 6 <= bot_id < 12:
            if not self.graph_mobs['robots_blue'][bot_id - 6].pos().x() == x and \
                    not self.graph_mobs['robots_blue'][bot_id - 6].pos().y() == y:
                self.graph_mobs['robots_blue'][bot_id - 6].setPos(x, y)
                self.graph_mobs['robots_blue'][bot_id - 6].setRotation(math.radians(theta))
                self.graph_mobs['robots_numbers'][bot_id].setPos(x, y)
        self.show_bot(bot_id)

    def show_ball(self):
        """ Affiche la balle dans la fenêtre de terrain """
        self.graph_mobs['ball'].show()

    def show_bot(self, bot_id):
        """ Affiche un robot dans la fenêtre du terrain """
        if 0 <= bot_id < 6:
            self.graph_mobs['robots_yellow'][bot_id].show()
            if self.option_show_number:
                self.graph_mobs['robots_numbers'][bot_id].show()
            else:
                self.graph_mobs['robots_numbers'][bot_id].hide()
        elif 6 <= bot_id < 12:
            self.graph_mobs['robots_blue'][bot_id - 6].show()
            if self.option_show_number:
                self.graph_mobs['robots_numbers'][bot_id].show()
            else:
                self.graph_mobs['robots_numbers'][bot_id].hide()

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

    def show_select_bot(self, bot_id):
        """ Affiche le robot sélectionné """
        graph_bot = self.graph_mobs['robots_yellow'][bot_id] if bot_id < 6 else self.graph_mobs['robots_blue'][bot_id - 6]
        if not self.last_target == graph_bot:
            if self.last_target is not None:
                self.last_target.setPen(Qt.black)
            graph_bot.setPen(Qt.red)
            self.last_target = graph_bot

    def hide_select_bot(self):
        """ Cache le dernier robot sélectionné """
        if self.last_target is not None:
            if not self.parent.view_controller.page_tactic.isVisible():
                self.last_target.setPen(Qt.black)
                self.last_target = None
            else:
                self.last_target.setPen(Qt.black)

    def update_tactic_targeting(self):
        """ Met à jour la vue de la cible """
        if self.parent.view_controller.isVisible() and self.parent.view_controller.page_tactic.isVisible():
            if not self.graph_mobs['target'].isVisible():
                self.graph_mobs['target'].show()

            id_colored = int(self.parent.view_controller.selectRobot.currentText())
            self.show_select_bot(id_colored)

        else:
            self.hide_select_bot()
            if self.graph_mobs['target'].isVisible():
                self.graph_mobs['target'].hide()
# Under MIT License, see LICENSE.txt

import math

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Model.FrameModel import MyModelIndex

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(17)

        # Option
        self.vanishing = False

    def set_model(self, model):
        """ Ajoute le modèle de la vue """
        assert isinstance(model, QAbstractItemModel)
        self.model = model
        self.scene.addItem(self.graph_mobs['ball'])
        self.scene.addItem(self.graph_mobs['target'])
        for graphic_bot in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            self.scene.addItem(graphic_bot)
        for number in self.graph_mobs['robots_numbers']:
            self.scene.addItem(number)

    def refresh(self):
        """ Rafraîchit tous les paramètres des éléments graphiques de la fenêtre """
        if self.model is None:
            pass
        elif self.model.is_connected():
            num_frame = self.model.data(MyModelIndex(0, 0))
            if not num_frame == self.last_frame:
                self.refresh_ball()
                self.refresh_robots_blue()
                self.refresh_robots_yellow()
                self.last_frame = num_frame
                for bot in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
                        bot.setPen(Qt.black)
                if self.parent.view_controller.isVisible() and self.parent.view_controller.page_tactic.isVisible():
                    if not self.graph_mobs['target'].isVisible():
                        self.graph_mobs['target'].show()
                    id_colored = int(self.parent.view_controller.selectRobot.currentText())

                    if id_colored < 5:
                        self.graph_mobs['robots_yellow'][id_colored].setPen(Qt.red)
                    else:
                        self.graph_mobs['robots_blue'][id_colored - 6].setPen(Qt.red)
                else:
                    if self.graph_mobs['target'].isVisible():
                        self.graph_mobs['target'].hide()


    def refresh_ball(self):
        """ Rafraîchit les paramètre de la balle """
        try:
            x = self.model.data(MyModelIndex(1, 5))
            y = self.model.data(MyModelIndex(1, 6))
            if x is not None and y is not None:
                if not self.graph_mobs['ball'].isVisible():
                    self.graph_mobs['ball'].show()
                x, y, _ = self.model.field_info.convert_real_to_scene_pst(x, y)
                if not x == self.graph_mobs['ball'].pos().x() and not y == self.graph_mobs['ball'].pos().y():
                    self.graph_mobs['ball'].setPos(x, y)

            else:
                if self.vanishing:
                    self.graph_mobs['ball'].hide()
        except IndexError:
            if self.vanishing:
                self.graph_mobs['ball'].hide()

    def refresh_robots_yellow(self):
        """ Rafraîchit les paramètres des robots de l'équipe jaune """
        for id_bot in range(len(self.graph_mobs['robots_yellow'])):
            try:
                x = self.model.data(MyModelIndex(id_bot + 2, 5))
                y = self.model.data(MyModelIndex(id_bot + 2, 6))
                theta = self.model.data(MyModelIndex(id_bot + 2, 8))
                if x is not None and y is not None:
                    if not self.graph_mobs['robots_yellow'][id_bot].isVisible(): self.graph_mobs['robots_yellow'][id_bot].show()
                    x, y, theta = self.model.field_info.convert_real_to_scene_pst(x, y, theta=theta)
                    if not x == self.graph_mobs['robots_yellow'][id_bot].pos().x()\
                       and not y == self.graph_mobs['robots_yellow'][id_bot].pos().y():
                        self.graph_mobs['robots_yellow'][id_bot].setPos(x, y)
                        self.graph_mobs['robots_numbers'][id_bot].setPos(x + 5, y + 5)
                        self.graph_mobs['robots_yellow'][id_bot].setRotation(math.degrees(theta))
                else:
                    if self.vanishing:
                        self.graph_mobs['robots_yellow'][id_bot].hide()
            except IndexError:
                if self.vanishing:
                    self.graph_mobs['robots_yellow'][id_bot].hide()

    def refresh_robots_blue(self):
        """ Rafraîchit les paranètres des robots de l'équipe bleue """
        for id_bot in range(len(self.graph_mobs['robots_blue'])):
            try:
                x = self.model.data(MyModelIndex(id_bot + 8, 5))
                y = self.model.data(MyModelIndex(id_bot + 8, 6))
                theta = self.model.data(MyModelIndex(id_bot + 8, 8))

                if x is not None and y is not None:
                    if not self.graph_mobs['robots_blue'][id_bot].isVisible(): self.graph_mobs['robots_blue'][id_bot].show()
                    x, y, theta = self.model.field_info.convert_real_to_scene_pst(x, y, theta=theta)
                    if not x == self.graph_mobs['robots_blue'][id_bot].pos().x()\
                       and not y == self.graph_mobs['robots_blue'][id_bot].pos().y():
                        self.graph_mobs['robots_blue'][id_bot].setPos(x, y)
                        self.graph_mobs['robots_numbers'][id_bot + 6].setPos(x + 5, y + 5)
                        self.graph_mobs['robots_blue'][id_bot].setRotation(math.degrees(theta))
                else:
                    if self.vanishing:
                        self.graph_mobs['robots_blue'][id_bot].hide()
            except IndexError:
                if self.vanishing:
                    self.graph_mobs['robots_blue'][id_bot].hide()

    def mousePressEvent(self, event):
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

        # Élément graphique de la cible
        self.graph_mobs['target'] = QGraphicsPixmapItem(QPixmap('Img/ico-target.png'))
        self.graph_mobs['target'].setOffset(-55, -55)
        self.graph_mobs['target'].scale(0.21, 0.21)
        self.graph_mobs['target'].hide()

        # Élément graphique des robots jaunes
        self.graph_mobs['robots_yellow'] = [QGraphicsEllipseItem(-11.25, -11.25, 22.5, 22.5) for _ in range(6)]
        for robot_yellow in self.graph_mobs['robots_yellow']:
            robot_yellow.hide()
            robot_yellow.setSpanAngle(50000)
            robot_yellow.setBrush(QBrush(QColor(255, 255, 105)))
            robot_yellow.setPen(QPen(QColor(0, 0, 0)))

        # Élément graphique des robots bleus
        self.graph_mobs['robots_blue'] = [QGraphicsEllipseItem(-11.25, -11.5, 22.5, 22.5) for _ in range(6)]
        for robots_blue in self.graph_mobs['robots_blue']:
            robots_blue.hide()
            robots_blue.setSpanAngle(50000)
            robots_blue.setBrush(QBrush(QColor(105, 255, 255)))
            robots_blue.setPen(QPen(QColor(0, 0, 0)))

        # Élément graphique des nombres au dessus des robots
        self.graph_mobs['robots_numbers'] = [QGraphicsTextItem(str(x)) for x in range(12)]
        for number in self.graph_mobs['robots_numbers']:
            font = QFont()
            font.setBold(True)
            number.setFont(font)
            number.setPos(-6666, -6666)
            number.hide()

    def change_vanish_option(self):
        """ Option qui rend apparent la disparition des robots """
        self.vanishing = not self.vanishing

    def show_number_option(self):
        """ Option qui affiche ou cache les numéros des robots """
        if self.graph_mobs['robots_numbers'][0].isVisible():
            for number in self.graph_mobs['robots_numbers']:
                number.hide()
        else:
            for number in self.graph_mobs['robots_numbers']:
                number.show()

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

# Under MIT License, see LICENSE.txt

import math

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Model.FrameModel import MyModelIndex

__author__ = 'RoboCupULaval'


class FieldDisplay(QGraphicsView):
    def __init__(self):
        super(FieldDisplay, self).__init__()
        self.scene = QGraphicsScene(self)
        self.model = None
        self.last_frame = 0
        self.graph_mobs = dict()

        # Initialisation de l'interface
        self.init_draw_tools()
        self.init_graph_mobs()

        self.init_window()
        self.draw_field()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(20)

        # Option
        self.vanishing = False

    def set_model(self, model):
        assert isinstance(model, QAbstractItemModel)
        self.model = model
        self.scene.addItem(self.graph_mobs['ball'])
        self.scene.addItem(self.graph_mobs['target'])
        for graphic_bot in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            self.scene.addItem(graphic_bot)

    def refresh(self):
            if self.model is None:
                pass
            elif self.model.is_connected():
                num_frame = self.model.data(MyModelIndex(0, 0))
                if not num_frame == self.last_frame:
                    self.refresh_ball()
                    self.refresh_robots_blue()
                    self.refresh_robots_yellow()
                    self.last_frame = num_frame

    def refresh_ball(self):
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
                        self.graph_mobs['robots_yellow'][id_bot].setRotation(math.degrees(theta))
                else:
                    if self.vanishing:
                        self.graph_mobs['robots_yellow'][id_bot].hide()
            except IndexError:
                if self.vanishing:
                    self.graph_mobs['robots_yellow'][id_bot].hide()

    def refresh_robots_blue(self):
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
                        self.graph_mobs['robots_blue'][id_bot].setRotation(math.degrees(theta))
                else:
                    if self.vanishing:
                        self.graph_mobs['robots_blue'][id_bot].hide()
            except IndexError:
                if self.vanishing:
                    self.graph_mobs['robots_blue'][id_bot].hide()

    def mousePressEvent(self, event):
        x, y = self.model.field_info.convert_screen_to_real_pst(event.pos().x(), event.pos().y())
        self.model.add_target(x, y)
        x, y, _ = self.model.field_info.convert_real_to_scene_pst(x, y)
        self.graph_mobs['target'].setPos(x, y)

    def draw_field(self):
        self.scene.setSceneRect(-475, -325, 950, 650)

        # Dessin des lignes de délimitations du terrain
        self.scene.addRect(-450, -300, 900, 600, self.white_pen)
        self.scene.addLine(0, 300, 0, -300, self.white_pen)
        self.scene.addEllipse(-50, -50, 100, 100, self.white_pen)

    def init_draw_tools(self):
        self.white_pen = QPen(Qt.white)
        self.red_pen = QPen(Qt.red)

    def init_window(self):
        self.setFixedSize(1000, 700)
        self.scene.setSceneRect(-475, -325, 950, 650)
        self.scene.setBackgroundBrush(Qt.darkGreen)
        self.setScene(self.scene)

    def init_graph_mobs(self):
        # Élément graphique de la balle
        self.graph_mobs['ball'] = QGraphicsEllipseItem(-2.15, -2.15, 4.3, 4.3)
        self.graph_mobs['ball'].setBrush(QBrush(QColor(255, 92, 0)))
        self.graph_mobs['ball'].setPen(QPen(QColor(255, 92, 0)))

        # Élément graphique de la cible
        self.graph_mobs['target'] = QGraphicsPixmapItem(QPixmap('Img/ico-target.png'))
        self.graph_mobs['target'].setOffset(-55, -55)
        self.graph_mobs['target'].scale(0.21, 0.21)

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

    def change_vanish_option(self):
        self.vanishing = not self.vanishing
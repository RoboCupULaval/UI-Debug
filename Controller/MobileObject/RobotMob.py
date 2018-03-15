# Under MIT License, see LICENSE.txt

from math import cos
from math import atan2
from math import sin
from math import pi

from Controller.DrawingObject.Color import CLEAR_YELLOW, SKY_BLUE, RED, BLACK
from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class RobotMob(BaseMobileObject):
    def __init__(self, bot_id, team_color, x=0, y=0, theta=0):
        BaseMobileObject.__init__(self, x, y, theta)
        self._bot_id = bot_id
        self._team_color = team_color
        self._display_number = False
        self._display_select = False
        self._display_vector = False
        self._radius = 180 / 2

    def get_id(self):
        return self._bot_id

    def get_radius(self):
        return self._radius * QtToolBox.field_ctrl.ratio_field_mobs

    def show_speed_vector(self):
        self._display_vector = True

    def hide_speed_vector(self):
        self._display_vector = False

    def speed_vector_isVisible(self):
        return self._display_vector

    def draw(self, painter):
        # TODO Ajouter vecteur de direction
        if self.isVisible():
            x, y, theta = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y, self._theta)
            if self._team_color == 'yellow':
                painter.setBrush(QtToolBox.create_brush(color=CLEAR_YELLOW))
            else:
                painter.setBrush(QtToolBox.create_brush(color=SKY_BLUE))

            if self._display_select:
                painter.setPen(QtToolBox.create_pen(color=RED,
                                                    style='SolidLine',
                                                    width=2))
            else:
                painter.setPen(QtToolBox.create_pen(color=BLACK,
                                                    style='SolidLine',
                                                    width=1))

            radius = self.get_radius() * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)
            painter.drawLine(x, y, x + cos(theta) * radius, y + sin(theta) * radius)

            if self._display_number:
                painter.drawText(x + radius, y + radius * 2, '{:.1}{}'.format(self._team_color,self._bot_id))
            if self.speed_vector_isVisible():
                v_x, v_y = self._speed_vector
                x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x + v_x * 180, self._y + v_y * 180)
                painter.setPen(QtToolBox.create_pen(color=RED,
                                                    width=3))
                painter.drawLine(x, y, x2, y2)
                if (v_x ** 2 + v_y ** 2) > 0.05:
                    self._draw_vector_speed(painter)

    def _draw_vector_speed(self, painter):
        v_x, v_y = self._speed_vector
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x + v_x * 180, self._y + v_y * 180)
        angle = atan2(v_y, v_x) + pi / 2

        # flèche gauche
        arrow_x = x2 - 5 * sin(angle + pi / 4)
        arrow_y = y2 - 5 * cos(angle + pi / 4)
        painter.drawLine(x2, y2, arrow_x, arrow_y)

        # flèche droite
        arrow_x = x2 - 5 * sin(angle - pi / 4)
        arrow_y = y2 - 5 * cos(angle - pi / 4)
        painter.drawLine(x2, y2, arrow_x, arrow_y)

    def select(self):
        self._display_select = True

    def deselect(self):
        self._display_select = False

    def isSelect(self):
        return self._display_select

    def show_number(self):
        self._display_number = True

    def hide_number(self):
        self._display_number = False

    def number_isVisible(self):
        return self._display_number

    def show_effects(self):
        self._display_effects = True

    def hide_effects(self):
        self._display_effects = False

    def effects_isVisible(self):
        return self._display_effects

    @staticmethod
    def get_datain_associated():
        return 'robot'

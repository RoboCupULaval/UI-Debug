# Under MIT License, see LICENSE.txt

from math import cos
from math import sin

from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class RobotMob(BaseMobileObject):
    def __init__(self, bot_id, x=0, y=0, theta=0, is_yellow=True):
        BaseMobileObject.__init__(self, x, y, theta)
        self._id = bot_id
        self._is_yellow = is_yellow
        self._display_number = False
        self._display_select = False
        self._display_vector = False
        self._vector = (0, 0)
        self._radius = 180 / 2

    def draw(self, painter):
        # TODO Ajouter vecteur de direction
        if self.isVisible():
            x, y, theta = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y, self._theta)
            if self._is_yellow:
                painter.setBrush(QtToolBox.create_brush(color=(255, 255, 100)))
            else:
                painter.setBrush(QtToolBox.create_brush(color=(100, 150, 255)))

            if self._display_select:
                painter.setPen(QtToolBox.create_pen(color=(255, 0, 0),
                                                    style='SolidLine',
                                                    width=2))
            else:
                painter.setPen(QtToolBox.create_pen(color=(0, 0, 0),
                                                    style='SolidLine',
                                                    width=1))

            radius = self._radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)
            painter.drawLine(x, y, x + cos(theta) * radius, y + sin(theta) * radius)

            if self._display_number:
                painter.drawText(x + radius, y + radius * 2, str(self._id))

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
    def get_qt_item(drawing_data_in):
        return

    @staticmethod
    def get_datain_associated():
        return 'robot'

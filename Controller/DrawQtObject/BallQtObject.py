# Under MIT License, see LICENSE.txt

from Controller.BaseQtObject import BaseQtObject
from Controller.DrawQtObject.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class BallQtObject(BaseQtObject):
    def __init__(self, x=-999, y=-999):
        BaseQtObject.__init__(self)
        self._x = x
        self._y = y
        self._width = 5

    def draw(self, painter):
        if self.isVisible():
            painter.setBrush(QtToolBox.create_brush(color=(255, 100, 0)))
            painter.setPen(QtToolBox.create_pen(color=(0, 0, 0),
                                                style='SolidLine',
                                                width=1))
            painter.drawEllipse(self._x - self._width / 2,
                                self._y - self._width / 2,
                                self._width,
                                self._width)

    def setPos(self, x, y):
        x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(x, y)
        self._x = x
        self._y = y

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        return

    @staticmethod
    def get_datain_associated():
        return 'ball'

# Under MIT License, see LICENSE.txt

from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class BallMob(BaseMobileObject):
    def __init__(self, x=0, y=0):
        BaseMobileObject.__init__(self, x, y)
        self._radius = 43 / 2

    def draw(self, painter):
        if self.isVisible():
            painter.setBrush(QtToolBox.create_brush(color=(255, 100, 0)))
            painter.setPen(QtToolBox.create_pen(color=(0, 0, 0),
                                                style='SolidLine',
                                                width=1))
            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y)
            radius = self._radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius,
                                y - radius,
                                radius * 2,
                                radius * 2)

    @staticmethod
    def get_qt_item(drawing_data_in):
        return

    @staticmethod
    def get_datain_associated():
        return 'ball'

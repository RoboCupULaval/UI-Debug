# Under MIT License, see LICENSE.txt
from PyQt4.QtGui import QPainter
from Controller.BaseQtObject import BaseQtObject
from Controller.DrawQtObject.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawCircleDataIn import DrawCircleDataIn
from PyQt4 import QtGui
from PyQt4 import QtCore

__author__ = 'RoboCupULaval'


class RobotQtObject(BaseQtObject):
    def __init__(self, x=0, y=0, theta=0, is_yellow=True):
        BaseQtObject.__init__(self)
        self._x = x
        self._y = y
        self._theta = theta
        self._is_yellow = is_yellow

    def draw(self, painter):
        if self.isVisible():
            if self._is_yellow:
                painter.setBrush(QtToolBox.create_brush(color=(255, 255, 100)))
            else:
                painter.setBrush(QtToolBox.create_brush(color=(100, 100, 255)))

            painter.setPen(QtToolBox.create_pen(color=(0, 0, 0),
                                                style='SolidLine',
                                                width=1))
            painter.drawEllipse(self._x, self._y, 10, 10)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        return

    @staticmethod
    def get_datain_associated():
        return 'robot'

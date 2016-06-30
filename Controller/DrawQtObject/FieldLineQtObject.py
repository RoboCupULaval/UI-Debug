# Under MIT License, see LICENSE.txt
from PyQt4.QtGui import QPainter
from Controller.BaseQtObject import BaseQtObject
from Controller.DrawQtObject.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawCircleDataIn import DrawCircleDataIn
from PyQt4 import QtGui
from PyQt4 import QtCore

__author__ = 'RoboCupULaval'


class FieldLineQtObject(BaseQtObject):
    def __init__(self):
        BaseQtObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine la pelouze
            painter.setBrush(QtToolBox.create_brush(color=(0, 150, 0)))
            painter.drawRect(0, 0, 950, 650)

            # Dessine les lignes
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            painter.setPen(QtToolBox.create_pen(color=(255, 255, 255),
                                                style='SolidLine',
                                                width=2))
            painter.drawRect(25, 25, 900, 600)
            painter.drawLine(475, 25, 475, 625)
            painter.drawEllipse(475 - 50, 325 - 50, 100, 100)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        return

    @staticmethod
    def get_datain_associated():
        return 'field'

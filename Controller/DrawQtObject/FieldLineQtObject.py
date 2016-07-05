# Under MIT License, see LICENSE.txt
from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldLineQtObject(BaseDrawObject):
    def __init__(self):
        BaseDrawObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
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
        return 'field-lines'

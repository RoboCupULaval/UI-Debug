# Under MIT License, see LICENSE.txt
from Controller.DrawingObject.Color import DARK_GREEN_FIELD, GREEN_FIELD
from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldGroundDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine la pelouze
            painter.setPen(QtToolBox.create_pen(is_hide=True))
            painter.setBrush(QtToolBox.create_brush(color=DARK_GREEN_FIELD))
            painter.drawRect(0, 0, 9500, 6500)
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width, height = QtToolBox.field_ctrl.get_size_to_screen()
            width /= 10
            painter.setBrush(QtToolBox.create_brush(color=GREEN_FIELD))
            for i in range(0, 10, 2):
                painter.drawRect(x + width * i, y, width, height)

    @staticmethod
    def get_datain_associated():
        return 'field-ground'

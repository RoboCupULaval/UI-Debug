# Under MIT License, see LICENSE.txt
from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldGroundQtObject(BaseDrawObject):
    def __init__(self):
        BaseDrawObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine la pelouze
            painter.setPen(QtToolBox.create_pen(is_hide=True))
            painter.setBrush(QtToolBox.create_brush(color=(0, 150, 0)))
            painter.drawRect(0, 0, 9500, 6500)
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width, height = QtToolBox.field_ctrl.get_size_to_screen()
            width /= 10
            painter.setBrush(QtToolBox.create_brush(color=(0, 125, 0)))
            for i in range(0, 10, 2):
                painter.drawRect(x + width * i, y, width, height)


    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        return

    @staticmethod
    def get_datain_associated():
        return 'field-ground'

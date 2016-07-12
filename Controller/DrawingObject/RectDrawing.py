# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawRectDataIn import DrawRectDataIn

__author__ = 'RoboCupULaval'


class RectDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            data = self.data
            painter.setPen(QtToolBox.create_pen(color=data['color'],
                                                style=data['style'],
                                                width=data['width']))
            painter.setBrush(QtToolBox.create_brush(data['color']))
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['top_left'])
            x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['bottom_right'])
            rect_height = abs(x1 - x2)
            rect_width = abs(y1 - y2)
            painter.drawRect(min(x1, x2),
                             max(y1, y2),
                             rect_height,
                             rect_width)

    @staticmethod
    def get_datain_associated():
        return DrawRectDataIn.__name__

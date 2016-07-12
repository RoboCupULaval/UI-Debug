# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawLineDataIn import DrawLineDataIn

__author__ = 'RoboCupULaval'


class LineDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            painter.setPen(QtToolBox.create_pen(color=self.data['color'],
                                                style=self.data['style'],
                                                width=self.data['width']))
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['start'])
            x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['end'])
            painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return DrawLineDataIn.__name__

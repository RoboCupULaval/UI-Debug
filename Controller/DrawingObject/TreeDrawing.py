# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataModel.DrawingData.DrawTreeDataIn import DrawTreeDataIn

__author__ = 'RoboCupULaval'


class TreeDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            painter.setPen(QtToolBox.create_pen(color=self.data['color'],
                                                width=self.data['width']))
            painter.setBrush(QtToolBox.create_brush(is_visible=False))

            for node in self.data['tree']:
                x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*node[0])
                x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*node[1])
                painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return DrawTreeDataIn.__name__

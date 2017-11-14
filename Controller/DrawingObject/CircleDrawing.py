# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataObject.DrawingData.DrawCircleDataIn import DrawCircleDataIn

__author__ = 'RoboCupULaval'


class CircleDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            data = self.data
            painter.setPen(QtToolBox.create_pen(color=data['color'],
                                                style=data['style'],
                                                width=2 * QtToolBox.field_ctrl.ratio_screen))
            painter.setBrush(QtToolBox.create_brush(color=data['color']))
            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['center'])
            radius = data['radius'] * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius,
                                y - radius,
                                radius * 2,
                                radius * 2)

    @staticmethod
    def get_datain_associated():
        return DrawCircleDataIn.__name__

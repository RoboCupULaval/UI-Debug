# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataObject.DrawingData.DrawPointDataIn import DrawPointDataIn

__author__ = 'RoboCupULaval'


class PointDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            painter.setPen(QtToolBox.create_pen())
            painter.setBrush(QtToolBox.create_brush(color=self.data['color']))
            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['point'])
            radius = self.data['width'] * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius,
                                y - radius,
                                radius * 2,
                                radius * 2)

    @staticmethod
    def get_datain_associated():
        return DrawPointDataIn.__name__

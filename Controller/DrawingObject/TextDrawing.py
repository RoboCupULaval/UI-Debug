# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataObject.DrawingData.DrawTextDataIn import DrawTextDataIn

__author__ = 'RoboCupULaval'


class TextDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        # TODO Add alignment
        if self.isVisible():
            data = self.data
            painter.setPen(QtToolBox.create_pen(color=data['color'],
                                                width=data['size']))
            painter.setBrush(QtToolBox.create_brush(data['color']))
            painter.setFont(QtToolBox.create_font(style=data['font'],
                                                  width=data['size'],
                                                  is_bold=data['has_bold'],
                                                  is_italic=data['has_italic']))

            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['position'])
            painter.drawText(x, y, data['text'])

    @staticmethod
    def get_datain_associated():
        return DrawTextDataIn.__name__

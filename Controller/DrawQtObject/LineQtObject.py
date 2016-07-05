# Under MIT License, see LICENSE.txt

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawLineDataIn import DrawLineDataIn

__author__ = 'RoboCupULaval'


class LineQtObject(BaseDrawObject):
    def __init__(self, data_in):
        BaseDrawObject.__init__(self, data_in)

    def draw(self, painter):
        painter.setPen(QtToolBox.create_pen(color=self.data['color'],
                                            style=self.data['style'],
                                            width=self.data['width']))
        painter.setBrush(QtToolBox.create_brush(is_visible=False))
        x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['start'])
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['end'])
        painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du pinceau
        pen = QtToolBox.create_pen(color=draw_data['color'],
                                   style=draw_data['style'],
                                   width=draw_data['width'])

        # Création de l'objet
        return QtToolBox.create_line(draw_data['start'], draw_data['end'], pen)

    @staticmethod
    def get_datain_associated():
        return DrawLineDataIn.__name__

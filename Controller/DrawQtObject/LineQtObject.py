# Under MIT License, see LICENSE.txt

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawLineDataIn import DrawLineDataIn

__author__ = 'RoboCupULaval'


class LineQtObject(BaseDrawObject):
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

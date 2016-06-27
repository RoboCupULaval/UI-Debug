# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui

from Controller.BaseQtObject import BaseQtObject
from Controller.DrawQtObject.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawRectDataIn import DrawRectDataIn

__author__ = 'RoboCupULaval'


class RectQtObject(BaseQtObject):
    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du pinceau
        pen = QtToolBox.create_pen(color=draw_data['color'],
                                   style=draw_data['style'],
                                   width=draw_data['width'])

        # Création de la brosse
        brush = QtToolBox.create_brush(draw_data['color'])

        # Création de l'objet
        rect_height = draw_data['top_left'][0] - draw_data['bottom_right'][0]
        rect_width = draw_data['bottom_right'][1] - draw_data['top_left'][1]
        qt_rect = QtToolBox.create_rect(*draw_data['top_left'],
                                        rect_width,
                                        rect_height,
                                        pen=pen,
                                        is_fill=draw_data['is_fill'],
                                        brush=brush)
        qt_rect.setZValue(-2)
        return qt_rect

    @staticmethod
    def get_datain_associated():
        return DrawRectDataIn.__name__

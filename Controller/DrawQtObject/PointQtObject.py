# Under MIT License, see LICENSE.txt

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawPointDataIn import DrawPointDataIn

__author__ = 'RoboCupULaval'


class PointQtObject(BaseDrawObject):

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du peintre
        pen = QtToolBox.create_pen()

        # Création de la brosse
        brush = QtToolBox.create_brush(color=draw_data['color'])

        # Création de l'objet
        x, y = draw_data['point']
        radius = draw_data['width']
        qt_object = QtToolBox.create_ellipse_item(x - radius,
                                                  y - radius,
                                                  radius * 2,
                                                  radius * 2,
                                                  pen=pen,
                                                  is_fill=True,
                                                  brush=brush,
                                                  opacity=1)
        qt_object.setZValue(-1)
        return qt_object

    @staticmethod
    def get_datain_associated():
        return DrawPointDataIn.__name__

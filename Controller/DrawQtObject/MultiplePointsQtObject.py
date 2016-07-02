# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawMultiplePointsDataIn import DrawMultiplePointsDataIn

__author__ = 'RoboCupULaval'


class MultipleLinesQtObject(BaseDrawObject):

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du pinceau
        pen = QtToolBox.create_pen()

        # Création de la brosse
        brush = QtToolBox.create_brush(color=draw_data['color'])

        # Création de l'objet
        qt_objet = QtGui.QGraphicsItemGroup()
        radius = draw_data['width']
        for point in draw_data['points']:
            x, y = point
            qt_objet.addToGroup(QtToolBox.create_ellipse_item(x - radius,
                                                              y - radius,
                                                              radius * 2,
                                                              radius * 2,
                                                              pen=pen,
                                                              is_fill=True,
                                                              brush=brush,
                                                              opacity=1))
        return qt_objet

    @staticmethod
    def get_datain_associated():
        return DrawMultiplePointsDataIn.__name__

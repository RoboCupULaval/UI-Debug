# Under MIT License, see LICENSE.txt

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DrawingDataIn.DrawCircleDataIn import DrawCircleDataIn
from PyQt4 import QtGui

__author__ = 'RoboCupULaval'


class CircleQtObject(BaseQtObject):

    @staticmethod
    def get_qt_object(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du peintre
        pen = QtGui.QPen()
        pen.setStyle(BaseQtObject.line_style_allowed[draw_data['style']])
        pen.setWidth(2)
        r, g, b = draw_data['color']
        pen.setColor(QtGui.QColor(r, g, b))

        # Création de l'objet
        x, y = draw_data['center']
        radius = draw_data['radius']
        qt_objet = QtGui.QGraphicsEllipseItem(x - radius, y - radius, radius * 2, radius * 2)
        qt_objet.setPen(pen)
        if draw_data['is_fill']:
            qt_objet.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b)))
            qt_objet.setOpacity(0.5)

        return qt_objet

    @staticmethod
    def get_datain_associated():
        return DrawCircleDataIn.__name__

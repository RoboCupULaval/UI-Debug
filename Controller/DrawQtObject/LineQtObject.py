# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DrawingDataIn.DrawLineDataIn import DrawLineDataIn

__author__ = 'RoboCupULaval'


class LineQtObject(BaseQtObject):
    @staticmethod
    def get_qt_object(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data
        pen = QtGui.QPen()
        pen.setStyle(BaseQtObject.line_style_allowed[draw_data['style']])
        pen.setWidth(draw_data['width'])
        r, g, b = draw_data['color']
        pen.setColor(QtGui.QColor(r, g, b))

        # Création de l'objet
        x1, y1 = draw_data['start']
        x2, y2 = draw_data['end']
        qt_obj = QtGui.QGraphicsLineItem(x1, y1, x2, y2)
        qt_obj.setPen(pen)
        return qt_obj

    @staticmethod
    def get_datain_associated():
        return DrawLineDataIn.__name__

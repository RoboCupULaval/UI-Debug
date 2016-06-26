# Under MIT License, see LICENSE.txt

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DrawingDataIn.DrawMultipleLinesDataIn import DrawMultipleLinesDataIn
from PyQt4 import QtGui

__author__ = 'RoboCupULaval'


class MultipleLinesQtObject(BaseQtObject):

    @staticmethod
    def get_qt_object(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data
        qt_objet = QtGui.QGraphicsItemGroup()

        pen = QtGui.QPen()
        pen.setStyle(BaseQtObject.line_style_allowed[draw_data['style']])
        pen.setWidth(draw_data['width'])
        r, g, b = draw_data['color']
        pen.setColor(QtGui.QColor(r, g, b))

        # Création de l'objet
        first_point = draw_data['points'][0]
        for sec_point in draw_data['points'][1:]:
            x1, y1 = first_point
            x2, y2 = sec_point
            qt_sub_obj = QtGui.QGraphicsLineItem(x1, y1, x2, y2)
            qt_sub_obj.setPen(pen)
            qt_objet.addToGroup(qt_sub_obj)
            first_point = sec_point

        return qt_objet

    @staticmethod
    def get_datain_associated():
        return DrawMultipleLinesDataIn.__name__

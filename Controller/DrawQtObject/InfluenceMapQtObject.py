# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DrawingDataIn.DrawInfluenceMapDataIn import DrawInfluenceMapDataIn

__author__ = 'RoboCupULaval'


class InfluenceMapQtObject(BaseQtObject):
    @staticmethod
    def get_qt_object(drawing_data_in):
        draw_data = drawing_data_in.data

        # Calcul de la taille des rectanbles
        nb_width, nb_height = draw_data['dimension']
        width, height = 900, 600
        ref_x, ref_y = -450, -300
        rect_width = width / nb_width
        rect_height = height / nb_height

        # Création du peintre
        pen = QtGui.QPen()
        pen.setStyle(Qt.NoPen)
        pen.setWidth(0)

        # Création de l'objet
        qt_obj = QtGui.QGraphicsItemGroup()
        for nb_line, line in enumerate(draw_data['field_data']):
            for nb_col, case in enumerate(line):
                qt_sub_obj = QtGui.QGraphicsRectItem(ref_x + rect_width * nb_col,
                                                     ref_y + rect_height * nb_line,
                                                     rect_width,
                                                     rect_height)
                color_value = int((case - draw_data['coldest_numb']) / (draw_data['hotest_numb'] - draw_data['coldest_numb']) * 255)
                r, g, b = color_value, color_value, color_value
                pen.setColor(QtGui.QColor(r, g, b))
                color = QtGui.QColor(r, g, b)
                qt_sub_obj.setPen(pen)
                qt_sub_obj.setBrush(QtGui.QBrush(color))
                qt_sub_obj.setOpacity(0.5)
                qt_obj.addToGroup(qt_sub_obj)
        return qt_obj

    @staticmethod
    def get_datain_associated():
        return DrawInfluenceMapDataIn.__name__

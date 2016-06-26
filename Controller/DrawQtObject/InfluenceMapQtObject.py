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

        RGB_max = 255, 0, 0
        RGB_min = 0, 255, 0
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
                color_value = InfluenceMapQtObject._convert_RGB_value_with_minmax(case,
                                                                                  draw_data['coldest_numb'],
                                                                                  draw_data['hotest_numb'],
                                                                                  RGB_min,
                                                                                  RGB_max)
                r, g, b = color_value, color_value, color_value
                pen.setColor(QtGui.QColor(r, g, b))
                color = QtGui.QColor(r, g, b)
                qt_sub_obj.setPen(pen)
                qt_sub_obj.setBrush(QtGui.QBrush(color))
                qt_sub_obj.setOpacity(0.5)
                qt_obj.addToGroup(qt_sub_obj)
        return qt_obj

    @staticmethod
    def _convert_RGB_value_with_minmax(value, value_min, value_max, RGB_min, RGB_max):
        value_r = InfluenceMapQtObject._convert_color_value_with_minmax(value, value_min, value_max, RGB_min[0], RGB_max[0])
        value_g = InfluenceMapQtObject._convert_color_value_with_minmax(value, value_min, value_max, RGB_min[1], RGB_max[1])
        value_b = InfluenceMapQtObject._convert_color_value_with_minmax(value, value_min, value_max, RGB_min[2], RGB_max[2])
        return value_r, value_g, value_b

    @staticmethod
    def _convert_color_value_with_minmax(value, value_min, value_max, color_min, color_max):
        pourcentage_value = (value - value_min) / (value_max - value_min)
        if color_max > color_min:
            return int((color_max - color_min) * pourcentage_value + color_min)
        else:
            return int((color_min - color_max) * (1 - pourcentage_value) + color_max)


    @staticmethod
    def get_datain_associated():
        return DrawInfluenceMapDataIn.__name__

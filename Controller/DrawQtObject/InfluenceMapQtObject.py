# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DrawingDataIn.DrawInfluenceMapDataIn import DrawInfluenceMapDataIn

__author__ = 'RoboCupULaval'


class InfluenceMapQtObject(BaseQtObject):
    @staticmethod
    def get_qt_object(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        # TODO - Ajouter la fonctionnalité FOCUS
        # TODO - Externaliser les fonctions pour les rendre disponibles à tous les objets si besoins
        # TODO - Ajouter des fonctions de créations d'objects primitifs (ligne, rectangle, cercle, etc.)
        # TODO - WARNING - Le flipping des axes n'est pas géré pour le moment et peu impacter les positions rectangles
        draw_data = drawing_data_in.data

        # Calcul de la taille des rectanbles
        nb_width, nb_height = draw_data['size']
        ref_x, ref_y = -(screen_width * screen_ratio) / 2, -(screen_height * screen_ratio) / 2
        rect_width = (screen_width * screen_ratio) / nb_width
        rect_height = (screen_height * screen_ratio) / nb_height

        RGB_max = draw_data['hotest_color']
        RGB_min = draw_data['coldest_color']
        # Création du peintre
        pen = QtGui.QPen()
        if draw_data['has_grid']:
            pen.setStyle(BaseQtObject.line_style_allowed[draw_data['grid_style']])
        else:
            pen.setStyle(Qt.NoPen)
        pen.setWidth(draw_data['grid_width'])
        pen.setColor(QtGui.QColor(draw_data['grid_color'][0],
                                  draw_data['grid_color'][1],
                                  draw_data['grid_color'][2]))
        # Création de l'objet
        qt_obj = QtGui.QGraphicsItemGroup()
        qt_obj.setZValue(-1)
        for nb_line, line in enumerate(draw_data['field_data']):
            for nb_col, case in enumerate(line):
                if case > draw_data['hotest_numb']:
                    case = draw_data['hotest_numb']
                if case < draw_data['coldest_numb']:
                    case = draw_data['coldest_numb']
                qt_sub_obj = QtGui.QGraphicsRectItem(ref_x + rect_width * nb_col,
                                                     ref_y + rect_height * nb_line,
                                                     rect_width,
                                                     rect_height)
                RGB_value = InfluenceMapQtObject._convert_RGB_value_with_minmax(case,
                                                                                  draw_data['coldest_numb'],
                                                                                  draw_data['hotest_numb'],
                                                                                  RGB_min,
                                                                                  RGB_max)
                r, g, b = RGB_value
                color = QtGui.QColor(r, g, b)
                qt_sub_obj.setPen(pen)
                qt_sub_obj.setBrush(QtGui.QBrush(color))
                qt_sub_obj.setOpacity(draw_data['opacity'] / 10.0)
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

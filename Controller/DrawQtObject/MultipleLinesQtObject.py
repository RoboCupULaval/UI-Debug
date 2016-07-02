# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawMultipleLinesDataIn import DrawMultipleLinesDataIn

__author__ = 'RoboCupULaval'


class MultipleLinesQtObject(BaseDrawObject):

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du pinceau
        pen = QtToolBox.create_pen(color=draw_data['color'],
                                   style=draw_data['style'],
                                   width=draw_data['width'])

        # Création de l'objet
        qt_objet = QtGui.QGraphicsItemGroup()
        first_point = draw_data['points'][0]
        for sec_point in draw_data['points'][1:]:
            qt_objet.addToGroup(QtToolBox.create_line(first_point, sec_point, pen))
            first_point = sec_point

        return qt_objet

    @staticmethod
    def get_datain_associated():
        return DrawMultipleLinesDataIn.__name__

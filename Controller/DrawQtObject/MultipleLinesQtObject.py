# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawMultipleLinesDataIn import DrawMultipleLinesDataIn

__author__ = 'RoboCupULaval'


class MultipleLinesQtObject(BaseDrawObject):
    def __init__(self, data_in):
        BaseDrawObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            painter.setPen(QtToolBox.create_pen(color=self.data['color'],
                                                style=self.data['style'],
                                                width=self.data['width']))
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['points'][0])
            for sec_point in self.data['points'][1:]:
                x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*sec_point)
                painter.drawLine(x1, y1, x2, y2)
                x1, y1 = x2, y2

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

# Under MIT License, see LICENSE.txt
from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawCircleDataIn import DrawCircleDataIn

__author__ = 'RoboCupULaval'


class CircleQtObject(BaseDrawObject):
    def __init__(self, data_in):
        BaseDrawObject.__init__(self)
        self.data = data_in.data

    def draw(self, painter):
        if self.isVisible():
            data = self.data
            painter.setPen(QtToolBox.create_pen(color=data['color'],
                                                style=data['style'],
                                                width=2))
            painter.setBrush(QtToolBox.create_brush(color=data['color']))
            x, y = data['center']
            painter.drawEllipse(x - data['radius'],
                                y - data['radius'],
                                data['radius'] * 2,
                                data['radius'] * 2)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du peintre
        pen = QtToolBox.create_pen(color=draw_data['color'],
                                   style=draw_data['style'],
                                   width=2)

        # Création de la brosse
        brush = QtToolBox.create_brush(color=draw_data['color'])

        # Création de l'objet
        x, y = draw_data['center']
        qt_objet = QtToolBox.create_ellipse_item(x - draw_data['radius'],
                                                 y - draw_data['radius'],
                                                 draw_data['radius'] * 2,
                                                 draw_data['radius'] * 2,
                                                 pen=pen,
                                                 is_fill=draw_data['is_fill'],
                                                 brush=brush,
                                                 opacity=1)
        qt_objet.setZValue(-1)
        return qt_objet

    @staticmethod
    def get_datain_associated():
        return DrawCircleDataIn.__name__

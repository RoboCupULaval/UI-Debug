# Under MIT License, see LICENSE.txt

from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawRectDataIn import DrawRectDataIn

__author__ = 'RoboCupULaval'


class RectQtObject(BaseDrawObject):
    def __init__(self, data_in):
        BaseDrawObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            data = self.data
            painter.setPen(QtToolBox.create_pen(color=data['color'],
                                                style=data['style'],
                                                width=data['width']))
            painter.setBrush(QtToolBox.create_brush(data['color']))
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['top_left'])
            x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*data['bottom_right'])
            rect_height = abs(x1 - x2)
            rect_width = abs(y1 - y2)
            painter.drawRect(min(x1, x2),
                             max(y1, y2),
                             rect_height,
                             rect_width)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        draw_data = drawing_data_in.data

        # Création du pinceau
        pen = QtToolBox.create_pen(color=draw_data['color'],
                                   style=draw_data['style'],
                                   width=draw_data['width'])

        # Création de la brosse
        brush = QtToolBox.create_brush(draw_data['color'])

        # Création de l'objet
        rect_height = draw_data['top_left'][0] - draw_data['bottom_right'][0]
        rect_width = draw_data['bottom_right'][1] - draw_data['top_left'][1]
        qt_rect = QtToolBox.create_rect(*draw_data['top_left'],
                                        rect_width,
                                        rect_height,
                                        pen=pen,
                                        is_fill=draw_data['is_fill'],
                                        brush=brush)
        qt_rect.setZValue(-2)
        return qt_rect

    @staticmethod
    def get_datain_associated():
        return DrawRectDataIn.__name__

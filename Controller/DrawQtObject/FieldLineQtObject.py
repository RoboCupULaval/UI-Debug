# Under MIT License, see LICENSE.txt
from Controller.DrawQtObject.BaseDrawObject import BaseDrawObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldLineQtObject(BaseDrawObject):
    def __init__(self):
        BaseDrawObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine les lignes
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            painter.setPen(QtToolBox.create_pen(color=(255, 255, 255),
                                                style='SolidLine',
                                                width=2))
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width, height = QtToolBox.field_ctrl.get_size_to_screen()
            painter.drawRect(x, y, width, height)
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(0, 3000)
            x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(0, -3000)
            painter.drawLine(x1, y1, x2, y2)
            radius = 500 * QtToolBox.field_ctrl.ratio_screen
            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(0, 0)
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    @staticmethod
    def get_qt_item(drawing_data_in, screen_ratio=0.1, screen_width=9000, screen_height=6000):
        return

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

# Under MIT License, see LICENSE.txt

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QPainter

from Controller.DrawingObject.color import Color
from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox


class FieldLineDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

        self.field_cache = QPixmap(1000, 1000)
        self.field_painter = QPainter(self.field_cache)

    def draw(self, painter):
        if self.isVisible() and QtToolBox.field_ctrl.need_redraw:
            QtToolBox.field_ctrl.need_redraw = False
            # Grass drawing
            self.field_painter.setPen(QtToolBox.create_pen(is_hide=True))
            self.field_painter.setBrush(QtToolBox.create_brush(color=Color.DARK_GREEN_FIELD))
            self.field_painter.drawRect(0, 0, 9500, 6500)
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width, height = QtToolBox.field_ctrl.get_size_to_screen()
            width /= 10
            self.field_painter.setBrush(QtToolBox.create_brush(color=Color.GREEN_FIELD))
            for i in range(0, 10, 2):
                self.field_painter.drawRect(x + width * i, y, width, height)

            self.field_painter.setBrush(QtToolBox.create_brush(is_visible=False))

            self.field_painter.setPen(QtToolBox.create_pen(color=Color.WHITE,
                                                style='SolidLine',
                                                width=QtToolBox.field_ctrl.line_width * QtToolBox.field_ctrl.ratio_screen))

            for name, arc in QtToolBox.field_ctrl.field_arcs.items():
                self.drawArc(self.field_painter, arc)
            for name, line in QtToolBox.field_ctrl.field_lines.items():
                self.drawLine(self.field_painter, line)

            # Dessine left goal
            self.field_painter.setPen(QtToolBox.create_pen(color=Color.BLUE,
                                                style='SolidLine',
                                                width=50 * QtToolBox.field_ctrl.ratio_screen))
            for name, line in QtToolBox.field_ctrl.field_goal_left.items():
                self.drawLine(self.field_painter, line)

            # Dessine right goal
            self.field_painter.setPen(QtToolBox.create_pen(color=Color.YELLOW,
                                                style='SolidLine',
                                                width=50 * QtToolBox.field_ctrl.ratio_screen))
            for name, line in QtToolBox.field_ctrl.field_goal_right.items():
                self.drawLine(self.field_painter, line)

        painter.drawPixmap(0, 0, self.field_cache)

    def drawArc(self, painter,  arc):
        x, y, _  = QtToolBox.field_ctrl.convert_real_to_scene_pst(arc.center[0] - arc.radius,
                                                                  arc.center[1] + arc.radius)
        width = arc.radius * 2 * QtToolBox.field_ctrl.ratio_screen
        # Qt is weird and it require a rectangle to be defined to draw an arc
        rect = QtCore.QRect(x, y, width, width)
        # Angle are calculate in 1/16th of a degree
        painter.drawArc(rect,
                        int(arc.start_angle) * 16,
                        int(arc.end_angle - arc.start_angle) * 16)

    def drawLine(self, painter, line):
        x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p1[0], line.p1[1])
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p2[0], line.p2[1])

        painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

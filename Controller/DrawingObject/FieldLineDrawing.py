# Under MIT License, see LICENSE.txt
import math

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
            self.drawGrass()

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

    def drawGrass(self, nb_lines = 10):
        self.field_painter.setPen(QtToolBox.create_pen(is_hide=True))
        self.field_painter.setBrush(QtToolBox.create_brush(color=Color.DARK_GREEN_FIELD))
        self.field_painter.drawRect(0, 0, 9500, 6500)
        self.field_painter.setBrush(QtToolBox.create_brush(color=Color.GREEN_FIELD))

        width, height = QtToolBox.field_ctrl.field_length, QtToolBox.field_ctrl.field_width
        xo, yo = width / 2, height / 2
        width_line = width / nb_lines
        for i in range(0, nb_lines, 2):
            # Top left
            ax, ay, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(i * width_line - xo, -yo)
            # Bot right
            bx, by, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst((i + 1) * width_line -xo, height -yo)
            self.field_painter.drawRect(ax, ay, bx-ax, by-ay)


    def drawArc(self, painter,  arc):
        # Top left
        ax, ay, theta_off  = QtToolBox.field_ctrl.convert_real_to_scene_pst(arc.center[0] - arc.radius,
                                                                            arc.center[1] + arc.radius)
        # Lower right
        bx, by, _  = QtToolBox.field_ctrl.convert_real_to_scene_pst(arc.center[0] + arc.radius,
                                                                    arc.center[1] - arc.radius)
        # Qt is weird and it require a rectangle to be defined to draw an arc
        rect = QtCore.QRect(ax, ay, bx-ax, by-ay)

        # If the screen is rotate, the angle is also rotated
        theta_off_deg = theta_off * 180 / math.pi
        # Angle are calculate in 1/16th of a degree
        painter.drawArc(rect,
                        int(arc.start_angle - theta_off_deg) * 16,
                        int(arc.end_angle - arc.start_angle - theta_off_deg) * 16)

    def drawLine(self, painter, line):
        x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p1[0], line.p1[1])
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p2[0], line.p2[1])

        painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

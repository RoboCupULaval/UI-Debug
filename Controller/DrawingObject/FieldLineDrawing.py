# Under MIT License, see LICENSE.txt

from PyQt5 import QtCore

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldLineDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

    def drawArc(self, painter, arc_center, radius, start_angle, end_angle):
        x, y, _  = QtToolBox.field_ctrl.convert_real_to_scene_pst(arc_center[0] - radius,
                                                                  arc_center[1] + radius)
        #print(start_angle, end_angle)
        # Qt is weird and it require a rectangle to be defined to draw an arc
        r = QtCore.QRect(x, y,
                         radius * 2 * QtToolBox.field_ctrl.ratio_screen,
                         radius * 2 * QtToolBox.field_ctrl.ratio_screen)
        # Angle are calculate in 1/16th of a degree
        painter.drawArc(r, int(start_angle) * 16, int(end_angle - start_angle) * 16)

    def drawLine(self, painter, p1, p2):
        x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(p1[0], p1[1])
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(p2[0], p2[1])

        painter.drawLine(x1, y1, x2, y2)
    def draw(self, painter):
        if self.isVisible():
            # Dessine les lignes
            painter.setBrush(QtToolBox.create_brush(is_visible=False))

            # Rectangle de contour du terrain
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            length, width = QtToolBox.field_ctrl.get_size_to_screen()

            # Rectangle des buts
            goal_depth = QtToolBox.field_ctrl.goal_depth
            goal_width = QtToolBox.field_ctrl.goal_width

            goal_depth_resize = goal_depth * QtToolBox.field_ctrl.ratio_screen
            goal_width_resize = goal_width * QtToolBox.field_ctrl.ratio_screen
            x_goal = x - goal_depth_resize
            y_goal = y + width / 2 - goal_width_resize / 2
            painter.setPen(QtToolBox.create_pen(color=(0, 0, 255),
                                                style='SolidLine',
                                                width=3))
            painter.drawRect(x_goal, y_goal, goal_depth_resize, goal_width_resize)
            x_goal = x + length
            y_goal = y + width / 2 - goal_width_resize / 2
            painter.setPen(QtToolBox.create_pen(color=(255, 255, 0),
                                                style='SolidLine',
                                                width=3))
            painter.drawRect(x_goal, y_goal, goal_depth_resize, goal_width_resize)

            painter.setPen(QtToolBox.create_pen(color=(255, 255, 255),
                                                style='SolidLine',
                                                width= QtToolBox.field_ctrl.line_width * QtToolBox.field_ctrl.ratio_screen))

            # Dessine tous les arcs
            for name, arc in QtToolBox.field_ctrl.field_arcs.items():
                #print(name, arc.thickness)
                self.drawArc(painter, arc.center, arc.radius, arc.start_angle, arc.end_angle)
            for name, line in QtToolBox.field_ctrl.field_lines.items():
                #print(name, line.thickness)
                self.drawLine(painter, line.p1, line.p2)

            painter.setPen(QtToolBox.create_pen(color=(0, 0, 255),
                                                style='SolidLine',
                                                width=3))
            for name, line in QtToolBox.field_ctrl.field_goal_left.items():
                self.drawLine(painter, line.p1, line.p2)

            painter.setPen(QtToolBox.create_pen(color=(255, 255, 0),
                                                style='SolidLine',
                                                width=3))
            for name, line in QtToolBox.field_ctrl.field_goal_right.items():
                self.drawLine(painter, line.p1, line.p2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

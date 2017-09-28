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
                                                                  arc_center[1] - radius)
        #print(start_angle, end_angle)
        # Qt is weird and it require a rectangle to be defined to draw an arc
        r = QtCore.QRect(x, y,
                         radius * 2 * QtToolBox.field_ctrl.ratio_screen,
                         radius * 2 * QtToolBox.field_ctrl.ratio_screen)
        # Angle are calculate in 1/16th of a degree
        painter.drawArc(r, int(start_angle) * 16, int(end_angle - start_angle) * 16)
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

            # Rectangle de contour du terrain
            painter.drawRect(x, y, length, width)

            # Dessine tous les arcs
            """
            CenterCircle 0.0 360.00001001791264
            LeftFieldLeftPenaltyArc 0.0                  90.00000250447816                OK
            LeftFieldRightPenaltyArc 270.00000068324533 360.00001001791264
            RightFieldLeftPenaltyArc 180.00000500895632 270.00000068324533
            RightFieldRightPenaltyArc 90.00000250447816 180.00000500895632  Make a half-circle on the left
            """
            for name, arc in QtToolBox.field_ctrl.field_arcs.items():
                # if name == "RightFieldRightPenaltyArc":
                print(name, arc.center, arc.start_angle, arc.end_angle)
                self.drawArc(painter, arc.center, arc.radius, arc.start_angle, arc.end_angle)

            # Ligne de la surface de réparation
            rad_width = QtToolBox.field_ctrl.defense_radius * QtToolBox.field_ctrl.ratio_screen
            x_rad_goal = x
            y_rad_goal = y + width / 2 - QtToolBox.field_ctrl.defense_stretch / 2 * QtToolBox.field_ctrl.ratio_screen
            # => TopLeft
            if False:
                painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                             y_rad_goal - rad_width,
                                             rad_width * 2,
                                             rad_width * 2),
                                0, 90 * 16)


                y_rad_goal = y + width / 2 + QtToolBox.field_ctrl.defense_stretch / 2 * QtToolBox.field_ctrl.ratio_screen
                # => BotLeft
                painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                             y_rad_goal - rad_width,
                                             rad_width * 2,
                                             rad_width * 2),
                                270 * 16, 90 * 16)
                # => TopRight
                x_rad_goal = x + length
                y_rad_goal = y + width / 2 - QtToolBox.field_ctrl.defense_stretch / 2 * QtToolBox.field_ctrl.ratio_screen
                painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                             y_rad_goal - rad_width,
                                             rad_width * 2,
                                             rad_width * 2),
                                90 * 16, 90 * 16)
                # => BotRight
                x_rad_goal = x + length
                y_rad_goal = y + width / 2 + QtToolBox.field_ctrl.defense_stretch / 2 * QtToolBox.field_ctrl.ratio_screen
                painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                             y_rad_goal - rad_width,
                                             rad_width * 2,
                                             rad_width * 2),
                                180 * 16, 90 * 16)


            # Ligne de la surface de réparation (droite)
            goal_line_resized = QtToolBox.field_ctrl.defense_stretch * QtToolBox.field_ctrl.ratio_screen
            x1 = x + QtToolBox.field_ctrl.defense_radius * QtToolBox.field_ctrl.ratio_screen
            y1 = y + width / 2 - goal_line_resized / 2
            y2 = y + width / 2 + goal_line_resized / 2
            painter.drawLine(x1, y1, x1, y2)
            x1 = x + length - QtToolBox.field_ctrl.defense_radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawLine(x1, y1, x1, y2)

            # Ligne de demi-terrain
            x1, y1 = x + length / 2, y
            x2, y2 = x + length / 2, y + width
            painter.drawLine(x1, y1, x2, y2)

            # Ligne centrale longitudinale (d'un but à l'autre)
            x1, y1 = x, y + width/2
            x2, y2 = x + length,  y + width/2
            painter.drawLine(x1, y1, x2, y2)

            # Ligne penality 1
            ratio = QtToolBox.field_ctrl.ratio_screen
            dist_from_goal_line = QtToolBox.field_ctrl.penalty_line_from_spot_dist + QtToolBox.field_ctrl.penalty_spot_from_field_line_dist
            x1, y1 = x + dist_from_goal_line * ratio, y + width / 2 - 5  # TODO : faire selon la vision
            x2, y2 = x + dist_from_goal_line * ratio, y + width / 2 + 5
            painter.drawLine(x1, y1, x2, y2)

            # Ligne penality 2
            x1, y1 = x + length - dist_from_goal_line * ratio, y + width / 2 - 5  # TODO : faire selon la vision
            x2, y2 = x + length - dist_from_goal_line * ratio, y + width / 2 + 5
            painter.drawLine(x1, y1, x2, y2)

            # Cercle central
            radius = QtToolBox.field_ctrl.center_circle_radius * QtToolBox.field_ctrl.ratio_screen
            x, y = x + length / 2, y + width / 2
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

# Under MIT License, see LICENSE.txt

from PyQt5 import QtCore

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldLineDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine les lignes
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            painter.setPen(QtToolBox.create_pen(color=(255, 255, 255),
                                                style='SolidLine',
                                                width=2))

            # Rectangle de contour du terrain
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width, height = QtToolBox.field_ctrl.get_size_to_screen()
            painter.drawRect(x, y, width, height)

            # Rectangle des buts
            goal_width, goal_height = QtToolBox.field_ctrl.goal_size
            goal_width_resize = goal_width * QtToolBox.field_ctrl.ratio_screen
            goal_height_resize = goal_height * QtToolBox.field_ctrl.ratio_screen
            x_goal = x - goal_width_resize
            y_goal = y + height / 2 - goal_height_resize / 2
            painter.drawRect(x_goal, y_goal, goal_width_resize, goal_height_resize)
            x_goal = x + width
            y_goal = y + height / 2 - goal_height_resize / 2
            painter.drawRect(x_goal, y_goal, goal_width_resize, goal_height_resize)

            # Ligne de la surface de réparation
            rad_width = QtToolBox.field_ctrl.goal_radius * QtToolBox.field_ctrl.ratio_screen
            x_rad_goal = x
            y_rad_goal = y + height / 2 - QtToolBox.field_ctrl.goal_line / 2 * QtToolBox.field_ctrl.ratio_screen
            # => TopLeft
            painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                         y_rad_goal - rad_width,
                                         rad_width * 2,
                                         rad_width * 2),
                            0, 90 * 16)

            y_rad_goal = y + height / 2 + QtToolBox.field_ctrl.goal_line / 2 * QtToolBox.field_ctrl.ratio_screen
            # => BotLeft
            painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                         y_rad_goal - rad_width,
                                         rad_width * 2,
                                         rad_width * 2),
                            270 * 16, 90 * 16)
            # => TopRight
            x_rad_goal = x + width
            y_rad_goal = y + height / 2 - QtToolBox.field_ctrl.goal_line / 2 * QtToolBox.field_ctrl.ratio_screen
            painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                         y_rad_goal - rad_width,
                                         rad_width * 2,
                                         rad_width * 2),
                            90 * 16, 90 * 16)
            # => BotRight
            x_rad_goal = x + width
            y_rad_goal = y + height / 2 + QtToolBox.field_ctrl.goal_line / 2 * QtToolBox.field_ctrl.ratio_screen
            painter.drawArc(QtCore.QRect(x_rad_goal - rad_width,
                                         y_rad_goal - rad_width,
                                         rad_width * 2,
                                         rad_width * 2),
                            180 * 16, 90 * 16)


            # Ligne de la surface de réparation (droite)
            goal_line_resized = QtToolBox.field_ctrl.goal_line * QtToolBox.field_ctrl.ratio_screen
            x1 = x + QtToolBox.field_ctrl.goal_radius * QtToolBox.field_ctrl.ratio_screen
            y1 = y + height / 2 - goal_line_resized / 2
            y2 = y + height / 2 + goal_line_resized / 2
            painter.drawLine(x1, y1, x1, y2)
            x1 = x + width - QtToolBox.field_ctrl.goal_radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawLine(x1, y1, x1, y2)

            # Ligne de demi-terrain
            x1, y1 = x + width / 2, y
            x2, y2 = x + width / 2, y + height
            painter.drawLine(x1, y1, x2, y2)

            # Cercle central
            radius = QtToolBox.field_ctrl.radius_center * QtToolBox.field_ctrl.ratio_screen
            x, y = x + width / 2, y + height / 2
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'

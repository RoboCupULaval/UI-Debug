# Under MIT License, see LICENSE.txt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath

from Controller.DrawingObject.color import Color
from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox
from collections import deque

__author__ = 'RoboCupULaval'


class BallMob(BaseMobileObject):
    def __init__(self, x=0, y=0):
        BaseMobileObject.__init__(self, x, y)
        self._radius = 43 / 2

        NB_BALL_POSE_TO_KEEP = 50
        self.queue = deque(maxlen=NB_BALL_POSE_TO_KEEP)

    @property
    def radius(self):
        return self._radius * QtToolBox.field_ctrl.ratio_field_mobs

    def draw(self, painter):
        if self.isVisible():
            bx, by, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y)

            self.queue.appendleft((self._x, self._y))

            # Draw ball's trail
            path_painter = QPainterPath()
            path_painter.moveTo(bx, by)
            for rx, ry in self.queue:
                x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(rx, ry)
                path_painter.lineTo(x, y)

            painter.setBrush(Qt.NoBrush)
            painter.setPen(QtToolBox.create_pen(color=Color.CLEAR_ORANGE,
                                                style='SolidLine',
                                                width=2))
            painter.drawPath(path_painter)

            # Draw ball
            painter.setBrush(QtToolBox.create_brush(color=Color.ORANGE))
            painter.setPen(QtToolBox.create_pen(color=Color.BLACK,
                                                style='SolidLine',
                                                width=1))
            radius = self.radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(bx - radius,
                                by - radius,
                                radius * 2,
                                radius * 2)


    @staticmethod
    def get_datain_associated():
        return 'ball'

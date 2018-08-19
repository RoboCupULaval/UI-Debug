# Under MIT License, see LICENSE.txt
from Controller.DrawingObject.color import Color
from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class FieldGroundDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

    def draw(self, painter):
        pass # TODO: REMOVE THIS WHOLE CLASS

    @staticmethod
    def get_datain_associated():
        return 'field-ground'

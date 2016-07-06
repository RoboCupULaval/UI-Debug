# Under GNU GPLv3 License, see LICENSE.txt

from math import cos, sin, atan2
from time import time
from abc import abstractmethod
from Controller.BaseQtObject import BaseQtObject

__author__ = 'jbecirovski'


class BaseMobileObject(BaseQtObject):
    def __init__(self, x=-9999, y=-9999, theta=0):
        BaseQtObject.__init__(self)
        self._x = x
        self._y = y
        self._last_vector_time = time()
        self._last_x = None
        self._last_y = None
        self._speed_vector = (0, 0)
        self._theta = theta

    def setPos(self, x, y):
        self._last_x, self._last_y = self._x, self._y
        self._x, self._y = x, y
        self._calculate_speed_vector()

    def _calculate_speed_vector(self):
        if self._last_x is not None and self._last_y is not None:
            cur_time = time()
            delta_t = cur_time - self._last_vector_time
            self._last_vector_time = cur_time
            self._speed_vector = (self._x - self._last_x) / (delta_t * 1000),\
                                 (self._y - self._last_y) / (delta_t * 1000)

    def setRotation(self, theta):
        self._theta = theta

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getRotate(self):
        return self._theta

    @abstractmethod
    def draw(self, painter):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_qt_item(drawing_data_in):
        raise NotImplementedError()

    @staticmethod
    def get_datain_associated():
        return None
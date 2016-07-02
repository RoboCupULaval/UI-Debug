# Under GNU GPLv3 License, see LICENSE.txt

from abc import abstractmethod
from Controller.BaseQtObject import BaseQtObject

__author__ = 'jbecirovski'


class BaseMobileObject(BaseQtObject):
    def __init__(self, x=-9999, y=-9999, theta=0):
        BaseQtObject.__init__(self)
        self._x = x
        self._y = y
        self._theta = theta

    def setPos(self, x, y):
        self._x = x
        self._y = y

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
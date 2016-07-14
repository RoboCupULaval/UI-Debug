# Under GNU GPLv3 License, see LICENSE.txt

from time import time
from Controller.AbstractDrawingObject import AbstractDrawingObject

__author__ = 'jbecirovski'


class BaseDrawingObject(AbstractDrawingObject):
    def __init__(self, data_in=None):
        AbstractDrawingObject.__init__(self)
        try:
            if data_in.data['timeout'] == 0:
                self._timeout = None
            else:
                self._timeout = data_in.data['timeout'] + time()
        except Exception as e:
            self._timeout = None
        self.data = data_in if data_in is None else data_in.data

    def time_is_up(self, p_time):
        if self._timeout is None:
            return False
        if p_time > self._timeout:
            return True
        else:
            return False

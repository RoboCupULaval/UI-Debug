# Under GNU GPLv3 License, see LICENSE.txt

from Controller.BaseQtObject import BaseQtObject

__author__ = 'jbecirovski'


class BaseDrawObject(BaseQtObject):
    def __init__(self, data_in=None):
        BaseQtObject.__init__(self)
        self.data = data_in if data_in is None else data_in.data
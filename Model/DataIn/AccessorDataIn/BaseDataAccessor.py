# Under MIT License, see LICENSE.txt

from abc import abstractmethod

from Model.DataIn.DataInObject import DataInObject

__author__ = 'RoboCupULaval'


class BaseDataAccessor(DataInObject):
    def __init__(self, data_in):
        super().__init__(data_in)
        self.data = data_in['data']
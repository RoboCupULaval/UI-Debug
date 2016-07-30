# Under MIT License, see LICENSE.txt

from abc import abstractmethod
from Model.DataObject.BaseDataObject import BaseDataObject

__author__ = 'RoboCupULaval'


class BaseDataSending(BaseDataObject):
    def __init__(self, data_in):
        super().__init__(data_in)

    @staticmethod
    @abstractmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        raise NotImplementedError()



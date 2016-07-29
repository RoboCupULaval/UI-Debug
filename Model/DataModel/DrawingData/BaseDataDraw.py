# Under MIT License, see LICENSE.txt

from abc import abstractmethod
from Controller.AbstractDrawingObject import AbstractDrawingObject
from Model.DataModel.DataObject import DataObject

__author__ = 'RoboCupULaval'


class BaseDataDraw(DataObject):
    """ Données entrantes pour les paquets de données pour dessiner """
    line_style_allowed = AbstractDrawingObject.line_style_allowed

    def __init__(self, data_in):
        super().__init__(data_in)

    @staticmethod
    @abstractmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        raise NotImplementedError()

    @property
    def filter(self):
        return self._data['link']

    @staticmethod
    def _style_is_valid(style):
        """ Vérifie si le style de ligne est valide """
        try:
            assert style in BaseDataDraw.line_style_allowed
            return True
        except AssertionError:
            return False

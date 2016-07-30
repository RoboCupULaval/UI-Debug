# Under MIT License, see LICENSE.txt

from abc import abstractmethod

from Model.DataObject.BaseDataObject import BaseDataObject

__author__ = 'RoboCupULaval'


class BaseDataLog(BaseDataObject):
    display_type = {0: 'NOTSET',
                    1: 'DEBUG',
                    2: 'INFO',
                    3: 'WARNING',
                    4: 'ERROR',
                    5: 'FATAL'}

    def __init__(self, data_in):
        super().__init__(data_in)

    @staticmethod
    @abstractmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        """ Affiche le message sous forme d'une chaîne de caractères."""
        raise NotImplementedError()

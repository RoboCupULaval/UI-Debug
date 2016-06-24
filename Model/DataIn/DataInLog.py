# Under MIT License, see LICENSE.txt

from abc import abstractmethod

from .DataIn import DataIn

__author__ = 'RoboCupULaval'


class DataInLog(DataIn):
    display_type = {0: 'NOTSET',
                    1: 'DEBUG',
                    2: 'INFO',
                    3: 'WARNING',
                    4: 'ERROR',
                    5: 'FATAL'}

    def __init__(self, data_in):
        DataIn.__init__(self, data_in)
        self.data = data_in['data']

    @abstractmethod
    def __str__(self):
        """ Affiche le message sous forme d'une chaîne de caractères."""
        raise NotImplementedError()
# Under GNU GPLv3 License, see LICENSE.txt

import logging
from abc import abstractmethod
from datetime import datetime

__author__ = 'jbecirovski'


class TimeListState:
    """ BaseTimeList est un état qui est géré sous forme de liste indexé par du temps """
    def __init__(self, name):
        assert isinstance(name, str), "{}.name: {} n'a pas le format attendu (str)".format(TimeListState.__name__, name)
        self._name = name
        self._logger = logging.getLogger(self._name)
        self._state = dict()


    @abstractmethod
    def __getitem__(self, index):
        """ Récupère l'état à l'instant T ou l'index """
        raise NotImplementedError()

    @abstractmethod
    def append(self, data):
        """ Ajoute un paquet de données """
        raise NotImplementedError()

    def count(self):
        """ Retourne le nombre d'éléments de la liste """
        raise NotImplementedError()

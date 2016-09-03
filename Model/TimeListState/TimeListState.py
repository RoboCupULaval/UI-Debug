# Under GNU GPLv3 License, see LICENSE.txt

import logging
from datetime import datetime

__author__ = 'jbecirovski'


class TimeListState:
    """ BaseTimeList est un état qui est géré sous forme d'une liste indexé par un index et par du temps """
    def __init__(self, name, default_model, debug=True):
        assert isinstance(name, str), "{}.name: {} n'a pas le format attendu (str)".format(TimeListState.__name__, name)
        self._name = name
        self._logger = logging.getLogger(self._name)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self._state = [Node(default_model)]
        self._init_logger()

    def _init_logger(self):
        """ Initialisation du logger """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.debug('INIT: Logger')

    def __getitem__(self, index):
        """ Récupère l'état à l'instant T ou l'index """
        if isinstance(index, int):
            return self._state[index].state
        elif isinstance(index, datetime):
            return self._get_nearest(index).state
        else:
            raise IndexError()

    def __len__(self):
        """ Retourne le nombre d'éléments de la liste """
        return len(self._state)

    def _get_nearest(self, time):
        # TODO - Augmenter la rapidité de l'algorithme
        # \====> Peut être améliorée en ayant une approche par le milieu puisque les données sont ordonnées

        """ Récupère l'état le plus près du temps donné. L'algorithme parcours la liste élément par élément de la fin
            vers le début et s'arrête lorsqu'un noeud est temporellement plus près que le noeud suivant. """
        self._logger.debug('GET: Nearest with time = {}'.format(time))
        nearest = self._state[-1]
        for node in self._state[1::-1]:
            if abs(nearest.time - time) > abs(node.time - time):
                nearest = node
            else:
                self._logger.debug('GET: Nearest is index={}'.format(nearest.index))
                return nearest

    def append(self, state):
        """ Ajoute un paquet de données """
        self._state.append(Node(state, parent=self._state[-1]))


class Node:
    """
        Node est un noeud avec un index, temps de création et un lien avec le noeud qui le précède et le suit.
        /!\ Les Nodes sont en mode read-only
    """
    _length = 0

    def __init__(self, state, parent=None):
        self._index = Node._length
        Node._length += 1
        self._prev = parent
        self._next = None
        self._time = datetime.now()

        if self._prev is not None:
            self._prev.next = self
            self._state = self._prev.state
            self._state.update(state)
        else:
            self._state = state

    @property
    def index(self):
        return self._index

    @property
    def state(self):
        return self._state.copy()

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        assert isinstance(node, Node)
        assert self._next is None
        self._next = node

    @property
    def prev(self):
        return self._prev

    @property
    def time(self):
        return self._time

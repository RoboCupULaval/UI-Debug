# Under GNU GPLv3 License, see LICENSE.txt

import logging, copy
from datetime import datetime

__author__ = 'jbecirovski'


class TimeListState:
    """ BaseTimeList est un état qui est géré sous forme d'une liste indexé par un index et par du temps """
    def __init__(self, name, default_model, debug=False):
        assert isinstance(name, str), "{}.name: {} n'a pas le format attendu (str)".format(TimeListState.__name__, name)
        self._name = name
        self._logger = logging.getLogger(TimeListState.__name__ + '.' + self._name)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self._state = [Node(default_model)]
        self._init_logger()
        self._logger.debug('INIT: default_state: {}'.format(self._state[-1]))

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
            self._logger.debug('GET: item with index={}'.format(index))
            return self._state[index].state
        elif isinstance(index, datetime):
            self._logger.debug('GET: item with time={}'.format(index))
            node = self._get_nearest(index)
            if node is not None:
                return node.state
        else:
            raise IndexError()

    def __len__(self):
        """ Retourne le nombre d'éléments de la liste """
        length = len(self._state)
        self._logger.debug('GET: Length {}'.format(length))
        return length

    def _get_nearest(self, time):
        # TODO - Augmenter la rapidité de l'algorithme
        # \====> Peut être améliorée en ayant une approche par le milieu puisque les données sont ordonnées
        # \====> Peut être améliorée en gardant la dernière recherche (recherche locale)

        """ Récupère l'état le plus près du temps donné. L'algorithme parcours la liste élément par élément de la fin
            vers le début et s'arrête lorsqu'un noeud est temporellement plus près que le noeud suivant. """
        self._logger.debug('GET: searching nearest node with time = {}'.format(time))
        nearest = self._state[0]
        for node in self._state[1:]:
            if node.time < time:
                nearest = node
            else:
                self._logger.debug('GET: Nearest node is index={} | time={}'.format(nearest.index, nearest.time))
                return nearest

    def append(self, state):
        """ Ajoute un paquet de données """
        self._logger.debug('SET: append => {}'.format(state))
        self._state[0].state.update()
        self._state[0] = Node(state)
        #self._state.append(Node(state, parent=self._state[-1]))

    def copy(self):
        """ Récupère une copie intégrale du TimeListState pour éviter la corruption de la liste originale """
        self._logger.debug('GET: copy')
        new_state = []
        first_node = Node(self._state[0].state)
        first_node._index = self._state[0].index
        first_node._time = copy.deepcopy(self._state[0].time)
        new_state.append(first_node)
        for i, node in enumerate(self._state[1:], start=1):
            new_node = Node(node.state, parent=new_state[i - 1])
            new_node._index = node.index
            new_node._time = copy.deepcopy(node.time)
            new_state.append(new_node)
        new_time_list_state = TimeListState(self._name, self._state[0])
        new_time_list_state._state = new_state
        return new_time_list_state


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

    def __repr__(self):
        return str(self._state)

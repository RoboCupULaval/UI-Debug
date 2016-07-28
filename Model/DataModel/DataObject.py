# Under MIT License, see LICENSE.txt

import pickle
from abc import abstractmethod
from datetime import datetime


__author__ = 'RoboCupULaval'
__version__ = '1.0'


class FormatPackageError(Exception):
    """ Exception pour le formatage des paquets """
    pass


def catch_format_error(funct):
    """ Décorateur qui récupère le message d'erreur d'une méthode spécifiquement pour les données
        entrantes. """
    def error_caught(*args):
        try:
            return funct(*args)
        except Exception as e:
            raise FormatPackageError('{}'.format(e))
    return error_caught


class DataObject:
    def __init__(self, data_in):
        if data_in is not None:
            DataObject.package_is_valid(data_in)
            self._data = data_in
        else:
            self._data = self.get_default_dict()
        self._data['time'] = datetime.now()

    @property
    def data(self):
        """ Requête pour obtenir les données """
        return self._data['data']

    @property
    def name(self):
        """ Requête pour obtenir le nom du créateur """
        return self._data['name']

    @property
    def type(self):
        """ Requête pour obtenir le type """
        return self._data['type']

    @property
    def version(self):
        """ Requête pour obtenir la version """
        return self._data['version']

    @property
    def link(self):
        """ Requête pour obtenir le filtre / id du robot associé """
        return self._data['link']

    @property
    def time(self):
        """ Requête pour obtenir le temps """
        return self._data['time']

    def set_data(self, **kwargs):
        """ Assigne des données en passant des arguments optionnels (exemple: NomDonnées=Données """
        for key, value in kwargs.items():
            self._data['data'][key] = value
        self._format_data()
        return self

    @abstractmethod
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        raise NotImplementedError()

    @abstractmethod
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        raise NotImplementedError()

    @catch_format_error
    def _format_data(self):
        """ Vérifie les données et complète les données manquantes avec des valeurs par défauts """
        self._check_obligatory_data()
        self._check_optional_data()

    @staticmethod
    @abstractmethod
    def get_type():
        """ Associe un object DrawDataIn avec un DataModel à destination de la clé du catalogue de la DataInFactory """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        raise NotImplementedError()

    def get_default_dict(self):
        """ Retourne un dictionnaire par défaut """
        p_type = self.get_type()
        p_data = self.get_default_data_dict()
        packet = dict(zip(['name', 'type', 'version', 'link', 'data'],
                          ['UI', p_type, __version__, None, p_data]))
        return packet

    def get_dict(self):
        """ Retourne une copie des données de l'objet sous forme de dictionnaire """
        return self._data.copy()

    def get_binary(self):
        """ Retourne le un version binaire des données de l'objet """
        return pickle.dumps(self._data)

    @staticmethod
    @catch_format_error
    def package_is_valid(data_in):
        assert isinstance(data_in, dict), \
            "package: {} n'est pas un disctionnaire.".format(type(data_in))
        keys = data_in.keys()
        assert 'name' in keys, \
            "package['name'] 'name' n'existe pas."
        assert isinstance(data_in['name'], str), \
            "paquet['name']: {} n'a pas le bon format (str).".format(type(data_in['name']))

        assert 'type' in keys, \
            "package['type'] 'type' n'existe pas."
        assert isinstance(data_in['type'], int), \
            "paquet['type']: {} n'a pas le bon format (int).".format(type(data_in['type']))
        assert 0 <= data_in['type'] < 7000, \
            "paquet['type']: {} n'a pas la bonne valeur (0 <= type < 7000)".format(data_in['type'])

        assert 'version' in keys, \
            "package['version'] 'version' n'existe pas."
        assert isinstance(data_in['version'], str), \
            "paquet['version']: {} n'a pas le bon format (str).".format(type(data_in['version']))
        assert data_in['version'] == __version__, \
            "paquet['version']: {} n'a pas la bonne valeur (version = {})".format(data_in['version'], __version__)

        assert 'link' in keys, \
            "package['link'] 'link' n'existe pas."
        if data_in['link'] is not None:
            assert isinstance(data_in['link'], (int, str)), \
                "paquet['link']: {} n'a pas le bon format (int).".format(type(data_in['link']))
        else:
            assert data_in['link'] is None, \
                "paquet['link']: {} n'a pas le bon format (None).".format(type(data_in['link']))

        assert 'data' in keys, \
            "package['data'] 'data' n'existe pas."
        assert isinstance(data_in['data'], dict), \
                "paquet['data']: {} n'a pas le bon format (dict).".format(type(data_in['data']))

    @staticmethod
    def _colorRGB_is_valid(color):
        """ Vérifie si une couleur RGB est valide """
        try:
            assert isinstance(color, tuple)
            assert len(color) == 3
            for value in color:
                assert 0 <= value <= 255
            return True
        except AssertionError:
            return False

    @staticmethod
    def _point_is_valid(point):
        """ Vérifie si un point est valide """
        try:
            assert isinstance(point, tuple)
            assert len(point) == 2
            for value in point:
                assert isinstance(value, int)
            return True
        except AssertionError:
            return False

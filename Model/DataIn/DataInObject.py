# Under MIT License, see LICENSE.txt

from abc import abstractmethod
from datetime import datetime

__author__ = 'RoboCupULaval'
__version__ = '1.0'


class DataInObject:
    def __init__(self, data_in):
        DataInObject.package_is_valid(data_in)
        self.name = data_in['name']
        self.type = data_in['type']
        self.version = data_in['version']
        self.link = data_in['link']
        self.time = datetime.now()

    @abstractmethod
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        raise NotImplementedError()

    @abstractmethod
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        raise NotImplementedError()

    def _format_data(self):
        """ Vérifie les données et complète les données manquantes avec des valeurs par défauts """
        try:
            self._check_obligatory_data()
            self._check_optional_data()
        except Exception as e:
            raise FormatPackageError(e)

    @staticmethod
    @abstractmethod
    def get_type():
        """ Associe un object DrawDataIn avec un DataIn à destination de la clé du catalogue de la DataInFactory """
        raise NotImplementedError()

    @staticmethod
    def package_is_valid(data_in):
        try:
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

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(DataInObject.__name__, e))

    def get_time(self):
        return self.time


class FormatPackageError(Exception):
    pass


def catch_format_error(funct):
    def error_caught(*args):
        try:
            return funct(*args)
        except Exception as e:
            raise FormatPackageError('{}'.format(e))
    return error_caught

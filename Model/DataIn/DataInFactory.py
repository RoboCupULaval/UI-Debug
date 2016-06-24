# Under MIT License, see LICENSE.txt
from .DataInObject import DataInObject

__author__ = 'RoboCupULaval'


class DataInFactory(object):
    def __init__(self):
        self._name = DataInFactory.__name__
        self._catalog_from_type_to_data_in_object = dict()
        self._init_object_catalog()

    def _init_object_catalog(self):
        """ Initialise le catalogue d'objet pour la factory """
        self._import_data_in_classes()
        for subclass in DataInObject.__subclasses__():
            for subsubclass in subclass.__subclasses__():
                self._catalog_from_type_to_data_in_object[subsubclass.get_type()] = subsubclass

    def _import_data_in_classes(self):
        """ Importe les objets dans les sous-dossiers de Model.DataIn """
        from os import listdir
        from os.path import isfile, join, isdir
        from importlib.machinery import SourceFileLoader

        path_current_dir = __file__.replace(DataInFactory.__name__ + '.py', '')
        folders_inside_current_dir = [f for f in listdir(path_current_dir)
                                      if isdir(join(path_current_dir, f)) and not f.count('_') and not f.count('Base')]
        for folder in folders_inside_current_dir:
            files = [f for f in listdir(join(path_current_dir, folder))
                     if isfile(join(path_current_dir, folder, f)) and f.count('_') == 0]
            for file in files:
                SourceFileLoader("", join(path_current_dir, folder, file)).load_module()

    def get_msg_bad_format(self, **kargs):
        """ Génère un LoggingMessage formaté pour recevoir des erreurs d'envoies de données """
        bad_log = self._catalog_from_type_to_data_in_object[2]({'name': self._name,
                                                                'type': 2,
                                                                'link': None,
                                                                'version': '1.0',
                                                                'data': {'level': 3, 'message': ''}})
        numb = False
        for key, item in sorted(kargs.items()):
            if numb:
                bad_log.data['message'] += '\n'
                numb = True
            bad_log.data['message'] += '{}: {}'.format(key, item)
        return bad_log

    def get_datain_object(self, data_in):
        """ Génère un DataIn en fonction du paquet reçu """
        try:
            DataInObject.package_is_valid(data_in)
            return self._catalog_from_type_to_data_in_object[data_in['type']](data_in)
        except Exception as e:
            return self.get_msg_bad_format(FormatPackageError=str(e), PaquetBrute=data_in)
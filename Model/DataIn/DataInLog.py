# Under MIT License, see LICENSE.txt

from datetime import date
from .DataIn import DataIn

__author__ = 'RoboCupULaval'


class DataInLog(DataIn):
    def __init__(self, name, type, data):
        DataIn.__init__(self, name, type, data)
        if not self.data_is_valid(name, type, data):
            raise AttributeError()
        self.display_type = {0: 'NOTSET',
                             1: 'DEBUG',
                             2: 'INFO',
                             3: 'WARNING',
                             4: 'ERROR',
                             5: 'FATAL'}

    def get_qt_object(self):
        # TODO : Générer l'object qt en question
        raise NotImplemented

    @staticmethod
    def data_is_valid(name, type, data):
        try:
            DataIn.package_is_valid(name, type)
            if type == 1:
                # Vérifie le format de données
                assert isinstance(data, dict)

                # Vérifie toutes les données
                for key, item in data.items():
                    assert isinstance(key, str)
                    assert isinstance(item, (int, str, float))

            elif type == 2:
                # Vérifie le format de données
                assert isinstance(data, dict)

                # Vérifie le level
                assert 'level' in data.keys()
                assert isinstance(data['level'], int)
                assert 0 <= data['level'] <= 5

                # Vérifie le message
                assert 'message' in data.keys()
                assert isinstance(data['message'], str)
            else:
                raise NotImplementedError()

            return True
        except BaseException:
            return False

    def __str__(self):
        message = ''
        if self.type == 1:
            for key, item in sorted(self.data.items()):
                message += '<{}> '.format(date.strftime(self.time, "%H:%M:%S"))
                message += '"{}": '.format(self.name)
                message += '{} = {}'.format(key, item) + '\n'
            message = message[:-1]

        elif self.type == 2:
            message += '<{}> '.format(date.strftime(self.time, "%H:%M:%S"))
            message += '"{}": '.format(self.name)
            message += "<{}> ".format(self.display_type[self.data['level']])
            message += self.data['message']

        return message

    def get_message(self):
        return self.data['message']

    def get_level(self):
        return self.data['level']
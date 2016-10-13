# Under MIT License, see LICENSE.txt
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending
from Model.DataObject.BaseDataObject import catch_format_error

# Demande à l'UI si le serveur de la stratégie IA est en UDP ou en serial

__author__='RobocupULaval'


class SendingAIServer(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data={} n'est pas un dictionnaire."
        keys = self.data.keys()
        assert 'is_serial' in keys, \
            "data['is_serial'] n'existe pas."
        assert isinstance(self.data['is_serial'], bool), \
            "data['is_serial']: {} n'a pas le format attendu (bool)".format(type(self.data['is_serial']))

        assert 'ip' in keys, \
            "data['ip'] n'existe pas."
        assert isinstance(self.data['ip'], str), \
            "data['ip']: {} n'a pas le format attendu (str)".format(type(self.data['ip']))

        assert 'port' in keys, \
            "data['port'] n'existe pas."
        assert isinstance(self.data['port'], int), \
            "data['port']: {} n'a pas le format attendu (int)".format(type(self.data['port']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['is_serial',
                         'ip',
                         'port'],
                        [False, str(), 0]))

    @staticmethod
    def get_type():
        return 5006

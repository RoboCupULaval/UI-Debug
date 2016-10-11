# Under MIT License, see LICENSE.txt
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending
from Model.DataObject.BaseDataObject import catch_format_error

# Demande à l'UI si le serveur de la stratégie IA est en UDP ou en serial

__author__='RobocupULaval'


class SendingAIServer(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(self, data_in)
        self._format_data(self)

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data={} n'est pas un dictionnaire."
        keys = self.data.keys()
        assert 'is_serial' in keys, \
            "data['is_serial'] n'existe pas."
        assert isinstance(self.data['is_serial'], bool), \
            "data['is_serial']: {} n'a pas le format attendu (bool)".format(type(self.data['is_serial']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['is_serial'],
                        [False]))

    @staticmethod
    def get_type():
        return 5006

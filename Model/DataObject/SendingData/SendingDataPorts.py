from Model.DataObject.SendingData.BaseDataSending import BaseDataSending
from Model.DataObject.BaseDataObject import catch_format_error

# Demande à l'UI si le serveur de la stratégie IA est en UDP ou en serial

__author__='RobocupULaval'


class SendingDataPorts(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data={} n'est pas un dictionnaire."
        keys = self.data.keys()

        assert 'recv_port' in keys, \
            "data['recv_port'] n'existe pas."
        assert isinstance(self.data['recv_port'], int), \
            "data['recv_port']: {} n'a pas le format attendu (int)".format(type(self.data['recv_port']))

        assert 'send_port' in keys, \
            "data['send_port'] n'existe pas."
        assert isinstance(self.data['send_port'], int), \
            "data['send_port']: {} n'a pas le format attendu (int)".format(type(self.data['send_port']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['recv_port',
                         'send_port'],
                         [0,
                          0]))

    @staticmethod
    def get_type():
        return 5007

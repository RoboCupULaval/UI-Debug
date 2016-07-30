# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingToggleHumanCtrl(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))

    @catch_format_error
    def _check_optional_data(self):
        keys = self.data.keys()
        if 'is_human_control' in keys:
            assert isinstance(self.data['is_human_control'], bool), \
                "data['is_human_control']: {} n'est pas le type attendu (bool)".format(type(self.data['is_human_control']))
        else:
            self.data['is_human_control'] = False

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return dict(zip(['is_human_control'],
                        [False]))

    @staticmethod
    def get_type():
        return 5001

# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingGeometry(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'width' in keys, \
            "data['width'] n'existe pas."
        assert isinstance(self.data['width'], (int, float)), \
            "data['width']: {} n'a pas le format attendu (int, float)".format(type(self.data['width']))
        assert 'height' in keys, \
            "data['height'] n'existe pas."
        assert isinstance(self.data['height'], (int, float)), \
            "data['height']: {} n'a pas le format attendu (int, float)".format(type(self.data['height']))
        assert 'center_radius' in keys, \
            "data['center_radius'] n'existe pas."
        assert isinstance(self.data['center_radius'], (int, float)), \
            "data['center_radius']: {} n'a pas le format attendu (int, float)".format(type(self.data['center_radius']))
        assert 'defense_radius' in keys, \
            "data['defense_radius'] n'existe pas."
        assert isinstance(self.data['defense_radius'], (int, float)), \
            "data['defense_radius']: {} n'a pas le format attendu (int, float)".format(type(self.data['defense_radius']))
        assert 'defense_stretch' in keys, \
            "data['defense_stretch'] n'existe pas."
        assert isinstance(self.data['defense_stretch'], (int, float)), \
            "data['defense_stretch']: {} n'a pas le format attendu (int, float)".format(type(self.data['defense_stretch']))
        assert 'goal_width' in keys, \
            "data['goal_width'] n'existe pas."
        assert isinstance(self.data['goal_width'], (int, float)), \
            "data['goal_width']: {} n'a pas le format attendu (int, float)".format(type(self.data['goal_width']))
        assert 'goal_height' in keys, \
            "data['goal_height'] n'existe pas."
        assert isinstance(self.data['goal_height'], (int, float)), \
            "data['goal_height']: {} n'a pas le format attendu (int, float)".format(type(self.data['goal_height']))
        assert 'ratio_field_mobs' in keys, \
            "data['ratio_field_mobs'] n'existe pas."
        assert isinstance(self.data['ratio_field_mobs'], (int, float)), \
            "data['ratio']: {} n'a pas le format attendu (int, float)".format(type(self.data['ratio_field_mobs']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return dict(zip(['width',
                         'height',
                         'center_radius',
                         'defense_radius',
                         'defense_stretch',
                         'goal_width',
                         'goal_height',
                         'ratio_field_mobs'],
                        [0 for _ in range(7)]+[1]))

    @staticmethod
    def get_type():
        return 5005

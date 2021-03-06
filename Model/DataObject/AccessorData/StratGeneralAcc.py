# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class StratGeneralAcc(BaseDataAccessor):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))

    @catch_format_error
    def _check_optional_data(self):
        keys = self.data.keys()
        if 'strategy' in keys:
            assert isinstance(self.data['strategy'], dict)
            for strategy_name, strategy_roles_dict in self.data['strategy'].items():
                assert isinstance(strategy_name, str)
                assert isinstance(strategy_roles_dict, dict)
                for role_type, roles in strategy_roles_dict.items():
                    assert role_type in ("required_roles", "optional_roles")
                    assert isinstance(roles, list)
                    for role in roles:
                        assert isinstance(role, str)
        else:
            self.data['strategy'] = None

        if 'tactic' in keys:
            assert isinstance(self.data['tactic'], list)
            for value in self.data['tactic']:
                assert isinstance(value, str)
        else:
            self.data['tactic'] = None

    @staticmethod
    def get_default_data_dict():
        return dict.fromkeys(('strategy', 'tactic'), None)

    @staticmethod
    def get_type():
        return 1001

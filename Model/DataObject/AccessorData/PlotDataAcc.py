# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class PlotDataAcc(BaseDataAccessor):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas une dict.".format(type(self.data))
        for key in self.data.keys():
            assert key in {'y_unit', 'y_label', 'x', 'y'}, \
                "data[{}] n'est pas une clé validee ('y_unit', 'y_label', 'x', 'y')".format(key)

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_type():
        return 1099



# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class FieldGeometryAcc(BaseDataAccessor):
    """ Paquet 2001: Demande de récupération des données géométrique du terrain """
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        pass

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict()

    @staticmethod
    def get_type():
        return 2001



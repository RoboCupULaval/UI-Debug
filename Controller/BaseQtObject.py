# Under MIT License, see LICENSE.txt

from abc import abstractmethod
from PyQt4.QtCore import Qt

__author__ = 'RoboCupULaval'


class BaseQtObject(object):
    line_style_allowed = {'SolidLine': Qt.SolidLine,
                           'DashLine': Qt.DashLine,
                           'DashDotLine': Qt.DashDotDotLine,
                           'DotLine': Qt.DotLine
                          }
    @staticmethod
    @abstractmethod
    def get_qt_object(drawing_data_in, screen_ratio=0.1, screen_width=900, screen_height=600):
        """ Génère un object Qt en fonction des données du DrawDataIn """
        raise NotImplementedError()


    @staticmethod
    @abstractmethod
    def get_datain_associated():
        """ Associe un object DrawDataIn avec un QtObject à destination de la clé du catalogue de la QtObjectFactory """
        raise NotImplementedError()

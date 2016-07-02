# Under MIT License, see LICENSE.txt

from abc import abstractmethod

from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class BaseQtObject(object):
    line_style_allowed = QtToolBox.line_style

    def __init__(self):
        self._visible = False

    def isVisible(self):
        return self._visible

    def hide(self):
        self._visible = False

    def show(self):
        self._visible = True

    @staticmethod
    @abstractmethod
    def get_qt_item(drawing_data_in):
        """ Génère un object Qt en fonction des données du DrawDataIn """
        raise NotImplementedError()


    @staticmethod
    @abstractmethod
    def get_datain_associated():
        """ Associe un object DrawDataIn avec un QtObject à destination de la clé du catalogue de la QtObjectFactory """
        raise NotImplementedError()

    @abstractmethod
    def draw(self, painter):
        """ Dessine l'objet à l'aide d'un QPainter """
        raise NotImplementedError()
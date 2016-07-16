# Under MIT License, see LICENSE.txt

from threading import Lock
from time import sleep, time
import pickle

from PyQt4.QtCore import QThread
from PyQt4.QtCore import QMutexLocker
from PyQt4.QtCore import QMutex

from Communication.UDPCommunication import UDPReceiving
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw
from Model.DataIn.LoggingDataIn.BaseDataInLog import BaseDataInLog
from Model.DataIn.AccessorDataIn.BaseDataAccessor import BaseDataAccessor
from Model.DataIn.AccessorDataIn.StratGeneralAcc import StratGeneralAcc
from Model.DataIn.AccessorDataIn.VeryLargeDataAcc import VeryLargeDataAcc
from .DataIn.DataInFactory import DataInFactory

__author__ = 'RoboCupULaval'


class DataInModel(object):
    def __init__(self, controller=None):
        # Initialisation
        self._controller = controller
        self._udp_receiver = UDPReceiving()
        self._datain_factory = DataInFactory()
        self._last_packet = None
        self._data_logging = list()
        self._data_config = list()
        self._data_draw = dict()
        self._data_STA = None
        self._mutex = QMutex()
        self._lock = Lock()
        self._data_recovery = QThread()

        self._start_time = time()

        self._initialization()

    def _initialization(self):
        """ Initialise la structure de données du DataInModel et des threads """
        self._data_draw['notset'] = list()
        self._data_draw['robots_yellow'] = [list() for _ in range(6)]
        self._data_draw['robots_blue'] = [list() for _ in range(6)]
        self._udp_receiver.start()
        self._data_recovery.run = self._get_data_in
        self._data_recovery.start()

    def _get_data_in(self):
        """ Récupère les données du serveur UDP pour les stocker dans le modèles """
        while True:
            QMutexLocker(self._mutex).relock()
            package = self._udp_receiver.get_last_data()
            try:
                self._extract_and_distribute_data(package)
            finally:
                self._last_packet = package[0] if package is not None else None
                QMutexLocker(self._mutex).unlock()
                sleep(0.01)

    def _extract_and_distribute_data(self, package):
        if package is not None:
            if isinstance(package, (tuple, list)):
                package = package[1]
            data_in = pickle.loads(package)
            if data_in is not None:
                data = self._datain_factory.get_datain_object(data_in)
                if isinstance(data, BaseDataInLog):
                    self._append_logging_datain(data)
                elif isinstance(data, BaseDataAccessor):
                    if isinstance(data, StratGeneralAcc):
                        if self._data_STA is not None:
                            for key in data.data.keys():
                                self._data_STA.data[key] = data.data[key]
                        else:
                            self._data_STA = data
                        self._controller.view_controller.refresh_strat(self._data_STA.data['strategy'])
                        self._controller.view_controller.refresh_tactic(self._data_STA.data['tactic'])
                    elif data.__class__.__name__ == VeryLargeDataAcc.__name__:
                        data.store()
                        self._extract_and_distribute_data(data.rebuild())
                elif isinstance(data, BaseDataInDraw):
                    self._data_draw['notset'].append(data)
                    self.show_draw(self._data_draw['notset'][-1])

    def _append_logging_datain(self, data):
        self._data_logging.append(data)
        self._controller.update_logging()

    def add_logging(self, name, message, level=2):
        data_in = {'name': name,
                   'type': 2,
                   'version': '1.0',
                   'link': None,
                   'data': {'level': level, 'message': message}
                   }
        self._append_logging_datain(self._datain_factory.get_datain_object(data_in))


    def _get_data(self, type=0):
        # TODO: A refactor
        QMutexLocker(self._mutex).relock()
        try:
            if type == 1:
                if len(self._data_logging):
                    return self._data_logging
                else:
                    return None
            elif type == 2:
                if isinstance(self._data_STA, DataInSTA):
                    return self._data_STA.data
                return None
            elif type == 3:
                return self._data_draw
            else:
                raise NotImplemented
        finally:
            QMutexLocker(self._mutex).unlock()

    def get_last_message(self):
        try:
            return self._get_data(1)[-1]
        except BaseException:
            return None

    def get_tactics(self):
        try:
            return self._get_data(2)['T']
        except:
            return None

    def get_strats(self):
        try:
            return self._get_data(2)['S']
        except:
            return None

    def get_last_log(self, index=0):
        if len(self._data_logging):
            return self._data_logging[index:]
        else:
            return None

    def show_draw(self, draw):
        if isinstance(draw, BaseDataInDraw):
            self._controller.add_draw_on_screen(draw)

    def save_logging(self, path, texte):
        with open(path, 'w') as f:
            texte = '##### LOGGING FROM UI #####\n' + texte
            f.write(texte)

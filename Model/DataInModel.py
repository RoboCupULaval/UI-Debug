# Under MIT License, see LICENSE.txt

import pickle
import logging
from time import time, sleep

from threading import Thread, Event

from Model.DataObject.AccessorData.StratGeneralAcc import StratGeneralAcc
from Model.DataObject.AccessorData.FieldGeometryAcc import FieldGeometryAcc
from Model.DataObject.AccessorData.RobotStateAcc import RobotStateAcc
from Model.DataObject.AccessorData.GameStateAcc import GameStateAcc
from Model.DataObject.AccessorData.VeryLargeDataAcc import VeryLargeDataAcc
from Model.DataObject.DataFactory import DataFactory
from Model.DataObject.DrawingData.BaseDataDraw import BaseDataDraw
from Model.DataObject.LoggingData.BaseDataLog import BaseDataLog
from Model.DataObject.AccessorData.HandShakeAcc import HandShakeAcc

from .TimeListState.TimeListState import TimeListState

__author__ = 'RoboCupULaval'


class DataInModel(Thread):
    def __init__(self, controller=None, debug=False):
        super().__init__()
        self._logger = logging.getLogger(DataInModel.__name__)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self._controller = controller
        self._recorder = None
        self._recorder_is_enable = False

        # Stockage de données
        self._data_logging = list()
        self._robot_state = TimeListState('RobotState', dict(zip(['yellow', 'blue'],
                                                                 [dict(zip(list(range(12)),
                                                                           [dict(zip(['tactic', 'action', 'target'],
                                                                                    ['None', 'None', 'None'])) for _ in range(12)]
                                                                           )) for _ in range(2)])))

        self._game_state = TimeListState('GameState', {'yellow': 'None', 'blue': 'None'})
        self._data_config = list()
        self._data_draw = dict()
        self._distrib_sepcific_packet = dict()
        self._data_STA_config = None

        # Système interne
        self._datain_factory = DataFactory()
        self._start_time = time()
        self.daemon = True

        # Événement
        self._event_robot_state = Event()
        self._event_game_state = Event()
        self._event_log = Event()
        self._event_draw = Event()
        self._event_pause = Event()

        # Réseau
        self._udp_receiver = None
        self._last_packet = None

        # Contrôleur
        self._pause = False

        # Initialisations
        self._init_distributor()
        self._init_logger()
        self._initialization()
        self.start()

    def _initialization(self):
        """ Initialise la structure de données du DataInModel et des threads """
        self._data_draw['notset'] = list()
        self._data_draw['robots_yellow'] = [list() for _ in range(12)]
        self._data_draw['robots_blue'] = [list() for _ in range(12)]
        self._logger.debug('INIT: object')


    def _init_distributor(self):
        """ Initialise la distribution des paquets en fonction du type de paquet """
        self._distrib_sepcific_packet[VeryLargeDataAcc.__name__] = self._distrib_VeryLargeData
        self._distrib_sepcific_packet[BaseDataDraw.__name__] = self._distrib_BaseDataDraw
        self._distrib_sepcific_packet[StratGeneralAcc.__name__] = self._distrib_StratGeneral
        self._distrib_sepcific_packet[BaseDataLog.__name__] = self._distrib_BaseDataLog
        self._distrib_sepcific_packet[HandShakeAcc.__name__] = self._distrib_HandShake
        self._distrib_sepcific_packet[RobotStateAcc.__name__] = self._distrib_RobotState
        self._distrib_sepcific_packet[GameStateAcc.__name__] = self._distrib_GameState
        self._distrib_sepcific_packet[FieldGeometryAcc.__name__] = self._distrib_FieldGeometry
        self._logger.debug('INIT: Distributor')

    def _init_logger(self):
        """ Initialisation du logger """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.debug('INIT: Logger')

    def setup_udp_server(self, udp_server):
        """ Installer le serveur UDP """
        self._udp_receiver = udp_server
        self._udp_receiver.start()
        self._event_pause.set()
        self._logger.debug('SETUP: UDP Server')

    def start(self):
        """ Exécute la boucle principale du Thread """
        self._logger.debug('START: Thread')
        super().start()

    def run(self):
        """ Récupère les données du serveur UDP pour les stocker dans le modèles """
        self._logger.debug('Thread RUNNING')
        while True:
            self.waiting_for_pause_event()
            package = None
            try:
                self._logger.debug('RUN: get Last data from udp server')
                package = self._udp_receiver.waiting_for_last_data()
                self._extract_and_distribute_data(package)
            except AttributeError as e:
                self._logger.warn(type(e).__name__ + str(e))
            finally:
                self._last_packet = package[0] if package is not None else None
        self._logger.debug('Thread RUN STOPPING')

    # === DISTRIBUTOR ===

    def _distrib_FieldGeometry(self, data):
        """ Traite le paque spécifique FieldGeometry """
        self._logger.debug('DISTRIB: FieldGeometry')
        self._controller.send_geometry()

    def _distrib_GameState(self, data):
        """ Traite le paquet spécifique GameState """
        self._logger.debug('DISTRIB: GameState')
        self._game_state.append(data.data)
        self._event_game_state.set()


    def _distrib_VeryLargeData(self, data):
        """ Traite le paquet spécifique VeryLargeData """
        self._logger.debug('DISTRIB: VeryLargeData')
        data.store()
        self._extract_and_distribute_data(data.rebuild())

    def _distrib_BaseDataDraw(self, data):
        """ Traite le paquet de type générique DataDraw """
        self._logger.debug('DISTRIB: BaseDataDraw')
        self._data_draw['notset'].append(data)
        self.show_draw(self._data_draw['notset'][-1])

    def _distrib_StratGeneral(self, data):
        """ Traite le paquet spécifique StratGeneral """
        self._logger.debug('DISTRIB: StratGeneral')
        if self._data_STA_config is not None:
            for key in data.data.keys():
                self._data_STA_config.data[key] = data.data[key]
        else:
            self._data_STA_config = data

    def _distrib_BaseDataLog(self, data):
        """ Traite le paquet de type générique BaseDataLog """
        self._logger.debug('DISTRIB: BaseDataLog')
        self._store_data_logging(data)

    def _distrib_HandShake(self, data):
        """ Traite le paquet spécifique HandShake """
        self._logger.debug('DISTRIB: HandShake')
        self._controller.send_handshake()

    def _distrib_RobotState(self, data):
        """ Traite le paquet spécifique RobotState """
        self._logger.debug('DISTRIB: RobotState')
        self._robot_state.append(data.data.copy())
        self._event_robot_state.set()

    # === PRIVATE METHODS ===

    def _extract_and_distribute_data(self, package):
        self._logger.debug('INTERNAL: Extract and distribute')
        if package is not None:
            if isinstance(package, (tuple, list)):
                package = package[1]
            data_in = pickle.loads(package)
            if data_in is not None:
                data = self._datain_factory.get_data_object(data_in)
                try:
                    if isinstance(data, BaseDataDraw):
                        self._distrib_sepcific_packet[BaseDataDraw.__name__](data)
                    elif isinstance(data, BaseDataLog):
                        self._distrib_sepcific_packet[BaseDataLog.__name__](data)
                    else:
                        self._distrib_sepcific_packet[type(data).__name__](data)
                except KeyError as e:
                    self._logger.warn(type(e).__name__, e)

    def _store_data_logging(self, data):
        """ Stock les données de logging """
        self._logger.debug('INTERNAL: Store logging')
        self._data_logging.append(data)
        self._controller.update_logging()

    # === PUBLIC METHODS ===

    def set_recorder(self, recorder):
        self._recorder = recorder

    def get_game_state_copy(self):
        return self._game_state.copy()

    def get_robot_state_copy(self):
        return self._robot_state.copy()

    def waiting_for_pause_event(self):
        self._logger.debug('WAITING FOR: Pause event')
        self._event_pause.wait()

    def waiting_for_robot_state_event(self):
        self._logger.debug('WAITING FOR: Robot State')
        if self._recorder_is_enable:
            sleep(1 / 30)
            self._logger.debug('CATCH: Recorded Robot State')
            return self._recorder.get_robot_state()
        else:
            self._logger.debug('CATCH: Robot State')
            self._event_robot_state.wait()
            self._event_robot_state.clear()
            return self._robot_state[-1]

    def waiting_for_game_state_event(self):
        self._logger.debug('WAITING FOR: Game State')
        if self._recorder_is_enable:
            sleep(1 / 30)
            self._logger.debug('CATCH: Recorded GameState')
            return self._recorder.get_game_state()
        else:
            self._logger.debug('CATCH: GameState')
            self._event_game_state.wait()
            self._event_game_state.clear()
            return self._game_state[-1]

    def add_logging(self, name, message, level=2):
        self._logger.debug('TRIGGER: Add new log')
        data_in = {'name': name,
                   'type': 2,
                   'version': '1.0',
                   'link': None,
                   'data': {'level': level, 'message': message}
                   }
        self._store_data_logging(self._datain_factory.get_data_object(data_in))

    def get_last_log(self, index=0):
        """ Récupère les derniers logging"""
        if len(self._data_logging):
            self._logger.debug('TRIGGER: GET LOG')
            return self._data_logging[index:]
        else:
            self._logger.warn('TRIGGER: GET LOG - No new log')
            return None

    def show_draw(self, draw):
        """ Afficher le dessin sur la fenêtre du terrain """
        if isinstance(draw, BaseDataDraw):
            self._logger.debug('TRIGGER: SHOW DRAW')
            self._controller.add_draw_on_screen(draw)
        else:
            self._logger.warn('TRIGGER: SHOW DRAW not available object')

    def write_logging_file(self, path, text):
        """ Écrit le logging dans un fichier texte sur le path déterminé """
        self._logger.debug('TRIGGER: write logging file')
        with open(path, 'w') as f:
            text = '##### LOGGING FROM UI #####\n' + text
            f.write(text)

    def pause(self):
        """ Met le modèle en pause """
        self._logger.debug('TRIGGER: PAUSE')
        self._event_pause.clear()

    def play(self):
        """ Met le modèle en lecture """
        self._logger.debug('TRIGGER: PLAY')
        self._event_pause.set()

    def is_pause(self):
        """ Requete pour savoir si le modèle est en pause """
        self._logger.debug('GET: is pause ?')
        return self._event_pause.isSet()

    # ====== RECORDER TOGGLE ======
    def enable_recorder(self):
        """ Activer l'enregistreur sur le modèle de frame """
        self._logger.debug('SET: Enable recorder')
        if self._recorder is not None:
            self._recorder.init(game_state=self.get_game_state_copy(), robot_state=self.get_robot_state_copy())
            self._recorder_is_enable = True
            self._event_game_state.set()
            self._event_robot_state.set()

    def disable_recorder(self):
        """ Désactiver l'enregistreur sur le modèle de frame """
        self._logger.debug('SET: Disable recorder')
        if self._recorder is not None:
            self._recorder_is_enable = False
            self._event_game_state.set()
            self._event_robot_state.set()
